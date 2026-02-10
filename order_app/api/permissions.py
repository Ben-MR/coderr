from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'

    def has_object_permission(self, request, view, obj):
        return obj.customer_user == request.user or obj.business_user == request.user
    
class IsBusinessUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.business_user == request.user
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser