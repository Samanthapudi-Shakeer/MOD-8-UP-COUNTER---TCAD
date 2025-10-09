"""Domain services for plan management."""
from __future__ import annotations

from typing import Iterable

from django.core.cache import cache

from accounts.models import UserProfile

from .models import Project, ProjectMembership
from .section_registry import TableConfig, find_table_config

CACHE_TTL = 60 * 10


def get_user_projects(user) -> Iterable[Project]:
    memberships = ProjectMembership.objects.filter(user=user).select_related("project")
    return [membership.project for membership in memberships]


def user_can_edit(user, project: Project) -> bool:
    if not user.is_authenticated:
        return False
    try:
        membership = ProjectMembership.objects.get(user=user, project=project)
    except ProjectMembership.DoesNotExist:
        return False
    if membership.can_edit:
        return True
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        return False
    return profile.is_editor


def cache_key_for_table(project: Project, table: TableConfig) -> str:
    return f"plan-table:{project.pk}:{table.key}"


def get_table_queryset(project: Project, table: TableConfig):
    model = table.model
    queryset = model.objects.filter(project=project)
    if hasattr(model, "exposure_history"):
        queryset = queryset.prefetch_related("exposure_history")
    if hasattr(model, "value_history"):
        queryset = queryset.prefetch_related("value_history")
    return queryset


def get_table_rows(project: Project, table_key: str):
    table = find_table_config(table_key)
    if not table:
        return []
    key = cache_key_for_table(project, table)
    cached = cache.get(key)
    if cached is not None:
        return cached
    queryset = get_table_queryset(project, table)
    rows = []
    for instance in queryset:
        row = {field: getattr(instance, field) for field in table.fields}
        row['id'] = instance.pk
        rows.append(row)
    if not rows and table.default_rows:
        rows = [dict(row, id=None) for row in table.default_rows]
    cache.set(key, rows, CACHE_TTL)
    return rows


def invalidate_table_cache(project: Project, table_key: str) -> None:
    table = find_table_config(table_key)
    if table:
        cache.delete(cache_key_for_table(project, table))
