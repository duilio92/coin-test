from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrOwnerReadOnly(BasePermission):
    """Admin can edit. Owner can see. Everyone else is rejected."""

    def has_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_staff or request.user == obj.user
        else:
            return request.user.is_staff