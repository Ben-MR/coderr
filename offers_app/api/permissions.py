from rest_framework.permissions import BasePermission
from order_app.api import permissions


class IsOwnOffer(BasePermission):
    """
    Object-level permission to only allow owners of an offer to edit or delete it.
    Assumes the model instance has a 'user_id' attribute.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.user_id == user.id
        )
    
class IsBusinessUser(permissions.BasePermission):
    """
    Global permission to only allow access to users registered as 'business' type.
    Ensures the user is authenticated and possesses the correct account designation.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.type == 'business'
        )