from django.db import models
from core import settings

class Reviews(models.Model):
    """
    Represents a review and rating left by a customer for a business user.

    Tracks the relationship between the reviewer and the professional service provider.
    Includes a numerical rating and a text description, with timestamps for 
    record-keeping and a uniqueness constraint to ensure integrity.
    """

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviewed_sales",
        db_column="business_user"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="written_reviews",
        db_column="reviewer"
    )
    rating = models.IntegerField(null=False, blank=False, default=0)
    description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Metadata and constraints for the Reviews model.
        
        Enforces a unique constraint to ensure that a reviewer can only 
        submit one review for a specific business user.
        """
        unique_together = ['business_user', 'reviewer']