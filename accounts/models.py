"""Models for user profile and permissions."""
from __future__ import annotations

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save


class UserProfile(models.Model):
    ROLE_VIEWER = "viewer"
    ROLE_EDITOR = "editor"
    ROLE_CHOICES = [
        (ROLE_VIEWER, "Viewer"),
        (ROLE_EDITOR, "Editor"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_VIEWER)

    def __str__(self) -> str:  # pragma: no cover - repr helper
        return f"{self.user.get_username()} ({self.get_role_display()})"

    @property
    def is_editor(self) -> bool:
        return self.role == self.ROLE_EDITOR

    @property
    def is_viewer(self) -> bool:
        return self.role == self.ROLE_VIEWER


User = get_user_model()


def ensure_profile(sender, instance: User, created: bool, **_: object) -> None:
    if created:
        UserProfile.objects.get_or_create(user=instance)


post_save.connect(ensure_profile, sender=get_user_model())
