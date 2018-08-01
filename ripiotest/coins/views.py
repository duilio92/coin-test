# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Coin, Account, CoinAccount
from .serializers import UserSerializer, CoinSerializer
from .serializers import AccountSerializer, CoinAccountSerializer
from .permissions import IsAdminOrUserReadOnlyPermission
from .permissions import IsReadOnlyPermission, CreateOrReadOnly
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def api_root(request, format=None):
    return Response({
        'users': reverse('api:user-list', request=request, format=format),
        'coins': reverse('coins:coin-list', request=request, format=format)
    })


@permission_classes((permissions.IsAdminUser,))
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User list and detail."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = permissions.AllowAny


@permission_classes((IsAdminOrUserReadOnlyPermission,))
class CoinViewSet(viewsets.ModelViewSet):
    """Coins list and detail. Admins can create coins."""

    queryset = Coin.objects.all()
    lookup_field = 'name'
    serializer_class = CoinSerializer


@permission_classes((IsReadOnlyPermission,))
class AccountViewSet(viewsets.ModelViewSet):
    """Clients account list and details."""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@permission_classes((CreateOrReadOnly,))
class CoinAccountViewSet(viewsets.ModelViewSet):
    """SubAccouns lists and details."""
    queryset = CoinAccount.objects.all()
    serializer_class = CoinAccountSerializer

#
# class CoinAccountViewSet(viewsets.ViewSet):
#     """
#     List all coinAccounts, or create a new coinAccount.
#     """
#     def list(self, request, format=None):
#         coinAccounts = coinAccount.objects.all()
#         serializer = coinAccountSerializer(coinAccounts, many=True, context={'request': request})
#         return Response(serializer.data)

#     def create(self, request, format=None):
#         serializer = coinAccountSerializer(data=request.data, context={'request': request})
#         if 
#         if serializer.is_valid():
#             self.save_coinAccount(serializer)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk, format=None):
#         coinAccount = self.get_object(pk)
#         serializer = coinAccountSerializer(coinAccount, context={'request': request})
#         return Response(serializer.data)

#     def get_object(self, pk):
#         try:
#             return coinAccount.objects.get(pk=pk)
#         except coinAccount.DoesNotExist:
#             raise Http404