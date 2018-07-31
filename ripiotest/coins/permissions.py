# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrOwnerReadOnlyPermission(BasePermission):
    """Admin can edit. Owner can see. Everyone else is rejected."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_staff or request.user == obj.user
        else:
            return request.user.is_staff


class IsAdminOrUserReadOnlyPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_logged_in
        else:
            return request.user.is_staff


class IsOwnerCreateOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            if request.method == 'CREATE':
                return request.user == obj.owner
            return True
