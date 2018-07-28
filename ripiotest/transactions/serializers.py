from rest_framework import serializers

from transactions.models import Transaction


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.origin + " to " + obj.destination

    class Meta:
        model = Transaction
        fields = (
            'url',
            'name',
            'date',
            'origin',
            'destination',
            'coin_type',
            'ammount'
        )# ,'transactions')
        extra_kwargs = {
            'url': {'view_name': 'transactions:transaction-detail'}}
