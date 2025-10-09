"""Admin registrations for plan models."""
from __future__ import annotations

from django.contrib import admin
from django.apps import apps

from . import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("created_at",)


@admin.register(models.ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "can_edit")
    list_filter = ("can_edit", "project")
    search_fields = ("project__name", "user__username")


# Dynamically register all BaseSection subclasses for convenience
section_models = [
    model for model in apps.get_app_config("plans").get_models()
    if issubclass(model, models.BaseSection) and model not in {models.Project, models.ProjectMembership}
]


for model in section_models:
    admin_class = type(
        f"{model.__name__}Admin",
        (admin.ModelAdmin,),
        {"list_display": [field.name for field in model._meta.fields if field.name not in {"project"}]},
    )
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        continue
