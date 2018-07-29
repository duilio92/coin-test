from rest_framework.permissions import BasePermission, SAFE_METHODS


class OwnerCreateOrReadOnly(BasePermission):
    """Owner can start a transacction,. Everyone else is rejected."""

    def has_base_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.is_staff
        return view.action == 'create' and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return (request.user.is_staff or
                    request.user == obj.destination.user or
                    request.user == obj.origin.user
                    )
