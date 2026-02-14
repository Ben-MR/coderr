from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from reviews_app.api.permissions import IsCustomer
from reviews_app.api.serializers import ReviewSerializer
from reviews_app.models import Reviews
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from rest_framework.exceptions import ValidationError

class ReviewFilter(django_filters.FilterSet):
    """
    Filter set for the Reviews model.
    Allows filtering reviews by the targeted business user or by 
    the customer who authored the review.
    """
    business_user_id = django_filters.NumberFilter(field_name='business_user')
    reviewer_id = django_filters.NumberFilter(field_name='reviewer')

    class Meta:
        model = Reviews
        fields = []

class ReviewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling review operations.
    Supports list, retrieval, creation, and modification of reviews.
    Includes duplicate check logic to ensure one review per business user per customer.
    """
    queryset = Reviews.objects.all()   
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering = ('-updated_at',) 
    ordering_fields = ['updated_at', 'rating', 'created_at']

    def get_permissions(self):
        """
        Assigns permissions based on the action.
        Restrict creation, updates, and deletion to authenticated customers 
        with ownership of the review.
        """
        if self.action in ["destroy", "partial_update"]:
            return [IsAuthenticated(), IsCustomer()]
        if self.action in "create":
            return [IsAuthenticated(), IsCustomer()]
        return super().get_permissions()

    
    def perform_create(self, serializer):
        """
        Saves a new review instance.
        Enforces business logic to prevent multiple reviews for the same business user 
        by the same reviewer. Automatically assigns the current user as the reviewer.
        """
        business_user = serializer.validated_data.get('business_user')
        reviewer = self.request.user
        already_reviewed = Reviews.objects.filter(
            business_user=business_user, 
            reviewer=reviewer
        ).exists()
        if already_reviewed:
            raise ValidationError("Du hast diesen Business-User bereits bewertet.")

        serializer.save(reviewer=reviewer)