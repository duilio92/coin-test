from rest_framework import serializers
from coins.models import Coin, Account, CoinAccount  # ,LANGUAGE_CHOICES, STYLE_CHOICES
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


class AcountSerializer(serializers.HyperlinkedModelSerializer):
    # coin_sub_accounts = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     view_name='coins:CoinAcount',
    #     read_only=True)
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user.username + " account"

    class Meta:
        model = Account
        fields = {'url', 'id', 'name', 'priv_key', 'pub_key'}# 'coin_sub_acounts'}
        extra_kwargs = {'url': {'view_name': 'coins:account-detail'}}