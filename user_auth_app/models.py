from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Usertype(models.TextChoices):
        CUSTOMER = "customer", "customer"
        BUSINESS = "business", "business"
    
    type = models.CharField(
        max_length=20,
        choices=Usertype.choices,
        default=Usertype.CUSTOMER,
    )



