from rest_framework.permissions import BasePermission



class IsOwnProfile(BasePermission):

    def has_object_permission(self, request, view, obj):

        user = request.user
        return (
            obj.created_by_id == user.id
        )