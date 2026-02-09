from django.db import models
from core import settings
from offers_app.models import OfferDetail
from offers_app.tests import User

class Order(models.Model):

    class StatusType(models.TextChoices):
        IN_PROGRESS = "in_progress", "in_progress"
        COMPLETED = "completed", "completed"

    
    offer_detail = models.ForeignKey(
        OfferDetail,
        on_delete=models.CASCADE,
        related_name="orders",
        db_column="offer_detail_id" 
    )   
    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sales",
        db_column="business_user"
    )
    customer_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="purchases",
        db_column="customer_user"
    )
    status = models.CharField(
        max_length=20,
        choices=StatusType.choices,
        default=StatusType.IN_PROGRESS,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
            unique_together = ['customer_user', 'offer_detail']