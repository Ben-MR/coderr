from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model for the Coderr platform.
    
    Extends Django's AbstractUser to include a 'type' field, allowing 
    the application to distinguish between customers and business providers 
    at the authentication level.
    """
    class Usertype(models.TextChoices):
        """
        Enumeration of available account types.
        - CUSTOMER: Standard user who purchases services.
        - BUSINESS: Professional user who offers software development services.
        """
        CUSTOMER = "customer", "customer"
        BUSINESS = "business", "business"
    
    type = models.CharField(
        max_length=20,
        choices=Usertype.choices,
        default=Usertype.CUSTOMER,
    )