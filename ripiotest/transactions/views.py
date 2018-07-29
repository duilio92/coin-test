# -*- coding: utf-8 -*-
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


# @permission_classes((permissions.readOnly,))
class TransactionViewSet(viewsets.ModelViewSet):
    """SubAccouns lists and details."""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    #permission_classes