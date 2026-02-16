from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    """
    Permission class to restrict access to customers.
    
    Global permission: Ensures the user is authenticated and has the 'customer' type.
    Object-level permission: Allows access if the user is either the customer 
    who placed the order or the business user who received it.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'

    def has_object_permission(self, request, view, obj):
        return obj.customer_user == request.user or obj.business_user == request.user
    
class IsBusinessUser(permissions.BasePermission):
    """
    Object-level permission for business users.
    
    Ensures that the requesting user is the specific business user 
    associated with the object (e.g., the provider of a service).
    """
    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user
    
class IsAdmin(permissions.BasePermission):
    """
    Permission class for administrative access.
    
    Global and object-level permission: Grants full access only to users 
    with superuser status.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
    
class IsOwnOrder(permissions.BasePermission):
    """
    Object-level permission to ensure users can only access their own orders.
    
    Grants access if the requesting user is either the customer who placed the order 
    or the business user who received it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.customer_user == request.user or obj.business_user == request.user