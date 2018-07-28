# -*- coding: utf-8 -*-
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from rest_framework import viewsets


class TransactionViewSet(viewsets.ModelViewSet):
    """SubAccouns lists and details."""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    #permission_classes