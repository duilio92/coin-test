from rest_framework import serializers
from coins.models import CoinAccount, Coin
from transactions.models import Transaction
from rest_framework.exceptions import ValidationError
from .tasks import create_transaction
from rest_framework.renderers import JSONRenderer


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.origin) + " to " + str(obj.destination)

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

    def create(self, validated_data):
        print "create was called"
        print validated_data
        ammount = validated_data["ammount"]
        origin = validated_data["origin"].pk
        destination = validated_data["destination"].pk
        coin_type = validated_data["coin_type"].pk
        print create_transaction.delay(
            ammount,
            origin,
            destination,
            coin_type)
        import pdb; pdb.set_trace()  # breakpoint 39e37cdb //

        #return Transaction.objects.create(**validated_data)

    def validate(self, data):
        if not data['origin']:
            raise ValidationError('La transaccion debe tener una cuenta origen')
        if not data['destination']:
            raise ValidationError('La transaccion debe tener una cuenta destino')
        if not data['ammount']:
            raise ValidationError('La transaccion debe tener un monto')
        if not data['coin_type']:
            raise ValidationError('La transaccion debe tener un tipo de moneda')
        origin = data['origin']
        destination = data['destination']
        ammount = data['ammount']
        coin_type = data['coin_type']
        if origin.main_account.user == destination.main_account.user:
            raise ValidationError('La transaccion debe ser entre dos usuarios distintos.')
        if (not origin.coin_type == coin_type
                or not destination.coin_type == coin_type):
            raise ValidationError('Ambas cuentas deben manejar el mismo tipo de moneda.')
        if ammount <= 0:
            raise ValidationError('La transaccion debe tener un monto mayor a 0.')
        if origin.balance - ammount <0:
            raise ValidationError('El origen no tiene fondos suficientes para la transaccion.')
        return data

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
            'url': {'view_name': 'api:transaction-detail'}}
