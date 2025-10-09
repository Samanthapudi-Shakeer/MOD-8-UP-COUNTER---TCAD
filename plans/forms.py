"""Dynamic form factories for plan sections."""
from __future__ import annotations

from django import forms
from django.db import models as dj_models
from django.forms import modelform_factory

from .section_registry import TableConfig


def build_form(table: TableConfig) -> type[forms.ModelForm]:
    widgets: dict[str, forms.Widget] = {}
    for field in table.model._meta.fields:
        if field.name in {"id", "project", "created_at", "updated_at"}:
            continue
        widget: forms.Widget
        if isinstance(field, dj_models.DateField):
            widget = forms.DateInput(attrs={"class": "form-control", "type": "date"})
        elif isinstance(field, (dj_models.TextField,)):
            widget = forms.Textarea(attrs={"class": "form-control", "rows": 3})
        elif isinstance(field, dj_models.BooleanField):
            widget = forms.CheckboxInput(attrs={"class": "form-check-input"})
        elif isinstance(field, (dj_models.FileField, dj_models.ImageField)):
            widget = forms.ClearableFileInput(attrs={"class": "form-control"})
        else:
            widget = forms.TextInput(attrs={"class": "form-control"})
        widgets[field.name] = widget

    form = modelform_factory(
        table.model,
        fields=[f for f in table.fields],
        widgets=widgets,
    )

    class TableForm(form):  # type: ignore[misc]
        pass

    return TableForm
