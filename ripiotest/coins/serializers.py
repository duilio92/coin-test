from rest_framework import serializers
from coins.models import Coin, Account, CoinAccount
from django.contrib.auth.models import User


class CoinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coin
        fields = ('url', 'id', 'name')
        extra_kwargs = {'url': {'view_name': 'coins:coin-detail'}}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username')
        extra_kwargs = {'url': {'view_name': 'coins:user-detail'}}


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    # coin_sub_accounts = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     view_name='coins:CoinAcount',
    #     read_only=True)
    name = serializers.SerializerMethodField()
    user = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='coins:user-detail',
        read_only=True)

    def get_name(self, obj):
        return obj.user.username + " account"

    class Meta:
        model = Account
        fields = ('url', 'name', 'user', 'pub_key')# 'coin_sub_acounts')
        extra_kwargs = {'url': {'view_name': 'coins:account-detail'}}


class CoinAccountSerializer(serializers.HyperlinkedModelSerializer):
    coin_type = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='coins:coin-detail',
        read_only=True)

    main_account = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='coins:account-detail',
        read_only=True)
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.main_account.user.username + " " + obj.coin_type.name

    class Meta:
        model = CoinAccount
        fields = ('url', 'name', 'balance', 'coin_type', 'main_account')# ,'transactions')
        extra_kwargs = {'url': {'view_name': 'coins:coinaccount-detail'}}
