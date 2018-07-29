from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.validators import UniqueValidator
from coins.models import Coin, Account, CoinAccount
from django.contrib.auth.models import User


class CoinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coin
        fields = ('url', 'id', 'name')
        extra_kwargs = {'url': {'view_name': 'api:coin-detail'}}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')
        extra_kwargs = {'url': {'view_name': 'api:user-detail'}}


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    sub_accounts = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='api:coinaccount-detail',
        read_only=True)
    name = serializers.SerializerMethodField()
    user = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='api:user-detail',
        queryset=User.objects.all(),
    )

    def get_name(self, obj):
        return obj.user.username + " account"

    def get_user(self, obj):
        return obj.user

    class Meta:
        model = Account
        fields = ('url', 'user', 'name', 'sub_accounts')
        extra_kwargs = {'url': {'view_name': 'api:account-detail'}}


class CoinAccountSerializer(serializers.HyperlinkedModelSerializer):
    #user = serializers.HiddenField(get)
    coin_type = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='api:coin-detail',
        queryset=Coin.objects.all()
    )

    main_account = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='api:account-detail',
        queryset=Account.objects.all())
    origin_transactions = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='api:transaction-detail',
        read_only=True
    )
    destination_transactions = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='api:transaction-detail',
        read_only=True
    )
    name = serializers.SerializerMethodField()
    balance = serializers.IntegerField(default=0, read_only=True)

    def get_user(self, obj):
        return obj.main_account.user

    def get_name(self, obj):
        return obj.main_account.user.username + " " + obj.coin_type.name

    class Meta:
        model = CoinAccount
        fields = ('url', 'name', 'balance', 'coin_type', 'main_account', 'origin_transactions', 'destination_transactions')
        extra_kwargs = {'url': {'view_name': 'api:coinaccount-detail'}}
        validators = [
            UniqueTogetherValidator(
                queryset=CoinAccount.objects.all(),
                fields=('main_account', 'coin_type')
            )
        ]
