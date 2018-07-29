# -*- coding: utf-8 -*-
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from transactions.permissions import OwnerCreateOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework import permissions


@permission_classes((OwnerCreateOrReadOnly,))
class TransactionViewSet(viewsets.ModelViewSet):
    """SubAccouns lists and details."""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
