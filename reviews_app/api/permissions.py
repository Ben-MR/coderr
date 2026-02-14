from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    """
    Permission class to restrict access to customers who own the specific object.

    Global permission: Ensures the user is authenticated and has the 'customer' account type.
    Object-level permission: Grants access only if the requesting user is the 
    actual author (reviewer) of the instance.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'

    def has_object_permission(self, request, view, obj):
        return obj.reviewer == request.user