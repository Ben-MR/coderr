from django.db import models
from django.conf import settings
  

class Offer(models.Model):
    """
    Represents a service offer created by a business user.
    Stores general information such as title, description, and an optional image.
    Maintains denormalized fields for minimum price and delivery time for performance.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='offer_images/', blank=True, null=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    min_delivery_time = models.IntegerField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_offers",
        help_text="User who owns and created the owned_offer."
    )

  
class OfferDetail(models.Model):
    """
    Represents a specific pricing tier for an Offer (Basic, Standard, or Premium).
    Contains details regarding revisions, delivery time, price, and specific features.
    Automatically updates the parent Offer's minimum price upon saving.
    """
        
    class OfferType(models.TextChoices):
        """
        Enumeration for different types of offer packages.
        """
        BASIC = "basic", "basic"
        STANDARD = "standard", "standard"
        PREMIUM = "premium", "premium"

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="details",
    )
    title = models.CharField(max_length=200)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(
        max_length=20,
        choices=OfferType.choices,
        default=OfferType.BASIC,
    )

    def save(self, *args, **kwargs):
        """
        Custom save method to recalculate the parent Offer's minimum price 
        whenever a detail tier is created or updated.
        """
        super().save(*args, **kwargs)
        self.offer.min_price = self.offer.details.aggregate(models.Min('price'))['price__min'] or 0
        self.offer.save()