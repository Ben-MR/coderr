from rest_framework.permissions import BasePermission


class IsOwnProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.user_id == user.id
        )