"""Views for project plan management."""
from __future__ import annotations

import json
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from accounts.models import UserProfile

from .forms import build_form
from .models import Project, ProjectMembership
from .section_registry import SECTIONS, TableConfig, find_table_config
from .services import get_table_rows, invalidate_table_cache, user_can_edit


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "plans/project_list.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            profile = self.request.user.userprofile
            can_edit_global = profile.is_editor
        except UserProfile.DoesNotExist:
            can_edit_global = False
        context["can_edit_global"] = can_edit_global
        return context


    def get_queryset(self):  # type: ignore[override]
        return Project.objects.filter(memberships__user=self.request.user).distinct()


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "plans/project_detail.html"
    context_object_name = "project"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        project = self.get_object()
        if not ProjectMembership.objects.filter(project=project, user=request.user).exists():
            return redirect("plans:project-list")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        try:
            profile = self.request.user.userprofile
            role = profile.role
        except UserProfile.DoesNotExist:
            role = UserProfile.ROLE_VIEWER
        context.update(
            {
                "sections": SECTIONS,
                "can_edit": user_can_edit(self.request.user, self.object),
                "user_role": role,
            }
        )
        return context


class SectionDataView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int, table_key: str) -> JsonResponse:
        project = get_object_or_404(Project, pk=pk)
        if not ProjectMembership.objects.filter(project=project, user=request.user).exists():
            return JsonResponse({"error": "Forbidden"}, status=403)
        table = find_table_config(table_key)
        if not table:
            return JsonResponse({"error": "Unknown table"}, status=404)
        rows = get_table_rows(project, table_key)
        field_metadata = [
            {
                "name": field,
                "label": table.model._meta.get_field(field).verbose_name.title(),
                "type": table.model._meta.get_field(field).get_internal_type(),
            }
            for field in table.fields
        ]
        return JsonResponse(
            {
                "rows": rows,
                "fields": field_metadata,
                "singleton": table.singleton,
                "table": table.key,
            }
        )


class SectionRowView(LoginRequiredMixin, View):
    http_method_names = ["post", "put", "patch", "delete"]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        project = get_object_or_404(Project, pk=kwargs["pk"])
        if not ProjectMembership.objects.filter(project=project, user=request.user).exists():
            return JsonResponse({"error": "Forbidden"}, status=403)
        self.project: Project = project
        return super().dispatch(request, *args, **kwargs)

    def _get_table(self, table_key: str) -> TableConfig:
        table = find_table_config(table_key)
        if not table:
            raise Http404("Unknown table")  # type: ignore[name-defined]
        return table

    def _json_data(self, request: HttpRequest) -> dict[str, Any]:
        if request.content_type == "application/json" and request.body:
            return json.loads(request.body)
        return request.POST.dict()

    def _get_instance(self, table: TableConfig, project: Project, row_id: int | None):
        model = table.model
        if table.singleton:
            instance, _ = model.objects.get_or_create(project=project)
            return instance
        if row_id is None:
            return None
        return get_object_or_404(model, pk=row_id, project=project)

    def post(self, request: HttpRequest, pk: int, table_key: str) -> JsonResponse:
        project: Project = self.project
        if not user_can_edit(request.user, project):
            return JsonResponse({"error": "Editing not permitted"}, status=403)
        table = self._get_table(table_key)
        form_class = build_form(table)
        data = self._json_data(request)
        instance = table.model(project=project)
        form = form_class(data, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.project = project
            obj.save()
            invalidate_table_cache(project, table_key)
            return JsonResponse({"success": True, "row": {field: getattr(obj, field) for field in table.fields}, "id": obj.pk})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    def put(self, request: HttpRequest, pk: int, table_key: str, row_id: int | None = None) -> JsonResponse:
        project: Project = self.project
        if not user_can_edit(request.user, project):
            return JsonResponse({"error": "Editing not permitted"}, status=403)
        table = self._get_table(table_key)
        instance = self._get_instance(table, project, row_id)
        if instance is None:
            return JsonResponse({"error": "Row not found"}, status=404)
        form_class = build_form(table)
        data = self._json_data(request)
        form = form_class(data, instance=instance)
        if form.is_valid():
            obj = form.save()
            invalidate_table_cache(project, table_key)
            return JsonResponse({"success": True, "row": {field: getattr(obj, field) for field in table.fields}, "id": obj.pk})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    patch = put

    def delete(self, request: HttpRequest, pk: int, table_key: str, row_id: int | None = None) -> JsonResponse:
        project: Project = self.project
        if not user_can_edit(request.user, project):
            return JsonResponse({"error": "Editing not permitted"}, status=403)
        table = self._get_table(table_key)
        if table.singleton:
            instance = self._get_instance(table, project, row_id)
            instance.delete()
            invalidate_table_cache(project, table_key)
            return JsonResponse({"success": True})
        if row_id is None:
            return JsonResponse({"error": "Row id required"}, status=400)
        instance = get_object_or_404(table.model, pk=row_id, project=project)
        instance.delete()
        invalidate_table_cache(project, table_key)
        return JsonResponse({"success": True})
