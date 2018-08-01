# -*- coding: utf-8 -*-
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from rest_framework import viewsets
from coins.permissions import CreateOrReadOnly
from django.db import transaction
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes


@permission_classes((CreateOrReadOnly,))
class CustomTransactionViewSet(viewsets.ViewSet):
    """
    List all transactions, or create a new transaction.
    """
    def list(self, request, format=None):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, format=None):
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            self.save_transaction(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def save_transaction(self, serializer):
        t = Transaction()
        t.origin = serializer.validated_data["origin"]
        t.destination = serializer.validated_data["destination"]
        t.ammount = serializer.validated_data["ammount"]
        t.coin_type = serializer.validated_data["coin_type"]
        if t.origin.balance - t.ammount < 0:
            raise Exception("El origen no tenia fondos")
        t.origin.balance = t.origin.balance - t.ammount
        t.destination.balance = t.destination.balance + t.ammount
        t.origin.save()
        t.destination.save()
        serializer.save()

    def retrieve(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, context={'request': request})
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404