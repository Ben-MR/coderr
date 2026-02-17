from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save  


class UserProfile(models.Model):
    """
    Extends the base User model with additional profile information.

    This model stores supplementary data for both customers and business users,
    including contact details, location, and professional descriptions. 
    It is linked to the authentication user via a OneToOne relationship.
    """
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

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        """
        Signal receiver to manage UserProfile lifecycle.
        """
        if created:
            UserProfile.objects.get_or_create(user=instance)
        
        if hasattr(instance, 'profile'):
            instance.profile.save()


    def __str__(self):
        """
        Return a human-readable representation of the profile.

        Uses the related user's username for display purposes
        (e.g. in Django Admin or debug output).
        """
        return self.user.username