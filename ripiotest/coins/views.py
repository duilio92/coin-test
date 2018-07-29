# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Coin, Account, CoinAccount
from .serializers import UserSerializer, CoinSerializer
from .serializers import AccountSerializer, CoinAccountSerializer
from .permissions import IsAdminOrUserReadOnlyPermission
from .permissions import IsAdminOrOwnerReadOnlyPermission
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
# from rest_framework import renderers
from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response


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
    serializer_class = CoinSerializer


@permission_classes((IsAdminOrOwnerReadOnlyPermission,))
class AccountViewSet(viewsets.ModelViewSet):
    """Clients account list and details."""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@permission_classes((IsAdminOrOwnerReadOnlyPermission,))
class CoinAccountViewSet(viewsets.ModelViewSet):
    """SubAccouns lists and details."""

    queryset = CoinAccount.objects.all()
    serializer_class = CoinAccountSerializer
