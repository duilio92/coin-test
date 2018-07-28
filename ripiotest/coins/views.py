# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.shortcuts import render
from django.contrib.auth.models import User
from coins.models import Coin, Account, CoinAccount
from coins.serializers import UserSerializer, CoinSerializer
from coins.serializers import AccountSerializer, CoinAccountSerializer
from coins.permissions import IsAdminOrOwnerReadOnlyPermission
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
        'coins': reverse('api:coin-list', request=request, format=format)
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User list and detail."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes((permissions.DjangoModelPermissionsOrAnonReadOnly,))
class CoinViewSet(viewsets.ModelViewSet):
    """Coins list and detail. Admins can create coins."""

    queryset = Coin.objects.all()
    serializer_class = CoinSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """Clients account list and details."""

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (IsAdminOrOwnerReadOnlyPermission,)


class CoinAccountViewSet(viewsets.ModelViewSet):
    """SubAccouns lists and details."""

    queryset = CoinAccount.objects.all()
    serializer_class = CoinAccountSerializer
    #permission_classes