# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrOwnerReadOnlyPermission(BasePermission):
    """Admin can edit. Owner can see. Everyone else is rejected."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_staff or request.user == obj.user
        else:
            return request.user.is_staff


class IsReadOnlyPermission(BasePermission):
    """
    Object-level permission to only allow read-only operations.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True


class IsAdminOrUserReadOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated()
        else:
            return request.user.is_staff


class IsOriginCreateOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.method == 'CREATE':
                return request.user == obj.origin.main_account.user
            return True
