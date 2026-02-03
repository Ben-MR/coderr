from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    ImageField = models.FileField(
        upload_to='profile_files/',
        blank=True,
        null=True,
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    tel = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    working_hours = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )



    def __str__(self):
        """
        Return a human-readable representation of the profile.

        Uses the related user's username for display purposes
        (e.g. in Django Admin or debug output).
        """
        return self.user.username
