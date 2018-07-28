from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
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
        #extra_kwargs = {'url': {'view_name': 'api:user-detail'}}


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    # coin_sub_accounts = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     view_name='api:CoinAcount',
    #     read_only=True)
    name = serializers.SerializerMethodField()
    user = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='api:user-detail',
        queryset=User.objects.all())

    def get_name(self, obj):
        return obj.user.username + " account"
    read_only_fields = ('pub_key')

    class Meta:
        model = Account
        fields = ('url', 'user', 'name', 'pub_key')# 'coin_sub_acounts')
        extra_kwargs = {'url': {'view_name': 'api:account-detail'}}


class CoinAccountSerializer(serializers.HyperlinkedModelSerializer):
    coin_type = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='api:coin-detail',
        queryset=Coin.objects.all())

    main_account = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='api:account-detail',
        queryset=Account.objects.all())
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.main_account.user.username + " " + obj.coin_type.name

    class Meta:
        model = CoinAccount
        fields = ('url', 'name', 'balance', 'coin_type', 'main_account')# ,'transactions')
        extra_kwargs = {'url': {'view_name': 'api:coinaccount-detail'}}
        validators = [
            UniqueTogetherValidator(
                queryset=CoinAccount.objects.all(),
                fields=('main_account', 'coin_type')
            )
        ]
