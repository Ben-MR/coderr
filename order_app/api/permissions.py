from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.type == 'customer'

    def has_object_permission(self, request, view, obj):
        return obj.customer_user == request.user or obj.business_user == request.user