from rest_framework.permissions import BasePermission

from order_app.api import permissions


class IsOwnOffer(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.user_id == user.id
        )
    
class IsBusinessUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.type == 'business'
        )