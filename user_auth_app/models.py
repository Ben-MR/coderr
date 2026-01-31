from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Usertype(models.TextChoices):
        CUSTOMER = "customer", "customer"
        BUSINESS_USER = "business-user", "business-user"
    
    type = models.CharField(
        max_length=20,
        choices=Usertype.choices,
        default=Usertype.CUSTOMER,
    )


    def __str__(self):
        """
        Return a human-readable representation of the profile.

        Uses the related user's username for display purposes
        (e.g. in Django Admin or debug output).
        """
        return self.user.username

