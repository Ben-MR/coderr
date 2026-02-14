from rest_framework.permissions import BasePermission


class IsOwnProfile(BasePermission):
    """
    Object-level permission to only allow users to edit or delete their own profile.
    
    This class verifies that the 'user_id' of the profile object matches 
    the ID of the currently authenticated user.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            obj.user_id == user.id
        )