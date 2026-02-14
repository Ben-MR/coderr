from django.db import models
from core import settings
from offers_app.models import OfferDetail

class Order(models.Model):
    """
    Represents a contractual agreement between a customer and a business user.
    
    This model tracks the lifecycle of a purchase, linking a specific OfferDetail 
    to both the buyer (customer_user) and the service provider (business_user).
    """

    class StatusType(models.TextChoices):
        """
        Defines the possible states of an order.
        - IN_PROGRESS: The service is currently being handled.
        - COMPLETED: The service has been successfully delivered.
        """
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
            """
            Database constraints for the Order model.
            Ensures that a customer can only place one active order per 
            specific offer detail to prevent accidental duplicates.
            """
            unique_together = ['customer_user', 'offer_detail']