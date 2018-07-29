from rest_framework import serializers
from coins.models import CoinAccount, Coin
from transactions.models import Transaction


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.origin + " to " + obj.destination

    origin = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='api:coinaccount-detail',
        queryset=CoinAccount.objects.all())

    destination = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='api:coinaccount-detail',
        queryset=CoinAccount.objects.all())
    coin_type = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='api:coin-detail',
        queryset=Coin.objects.all())

    date = serializers.DateTimeField(read_only=True)

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
