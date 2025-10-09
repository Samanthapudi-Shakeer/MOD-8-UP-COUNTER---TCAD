"""Context processors for plans app."""
from __future__ import annotations

from .section_registry import SECTIONS


def section_metadata(request):  # pylint: disable=unused-argument
    return {"plan_sections": SECTIONS}
