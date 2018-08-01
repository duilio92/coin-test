# -*- coding: utf-8 -*-
# from rest_framework.permissions import BasePermission, SAFE_METHODS
# from coins.models import CoinAccount


# # depracated
# class OwnerCreateOrReadOnly(BasePermission):
#     """Owner can start a transacction,. Everyone else is rejected."""

#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return request.user.is_staff
#         if view.action == 'create':
#             try:
#                 origin = CoinAccount.objects.get(
#                     pk=request.parser_context["kwargs"]["origin"]
#                 )
#                 return origin.main_account.user == request.user
#             except:
#                 return False

#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return (request.user.is_staff or
#                     request.user == obj.destination.user or
#                     request.user == obj.origin.user
#                     )
#         return False
