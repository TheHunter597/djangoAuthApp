from rest_framework.permissions import BasePermission

class IsSameUser(BasePermission):
    """Custom permission class to allow only owners to edit them."""
    message = "You must be the owner to do this."
    def has_object_permission(self, request, view, obj):
        """Return True if permission is granted to the user."""
        return obj.creator == request.user.id