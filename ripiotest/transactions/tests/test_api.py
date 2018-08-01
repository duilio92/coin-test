# -*- coding: utf-8 -*-
import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from coins.models import Coin, Account, CoinAccount
from django.contrib.auth.models import User


class TransactionTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testing",
            password="t3st1ng!!"
        )
        self.client = APIClient()
        # crear usuarios
        self.testUser1 = User.objects.create(
            username="user1",
            password="t3stfirst")
        self.testUser2 = User.objects.create(
            username="user2",
            password="t3stsecond")
        self.url_list_create = reverse('api:transaction-list')

        self.coin, created = Coin.objects.get_or_create(name="bitcoin")
        self.coin2, created = Coin.objects.get_or_create(name="testcoin")
        # crear cuentas de monedas
        self.ca_user1 = CoinAccount.objects.create(
            coin_type=self.coin,
            main_account=self.testUser1.account)
        self.ca_user1.balance = 1
        self.ca_user1.save()
        self.ca_user2 = CoinAccount.objects.create(
            coin_type=self.coin,
            main_account=self.testUser2.account)
        self.ca_different_coin = CoinAccount.objects.create(
            coin_type=self.coin2,
            main_account=self.testUser2.account)

        self.url_coin = reverse(
            'api:coin-detail',
            kwargs={'name': self.coin.name})
        self.url_account1 = reverse(
            'api:coinaccount-detail',
            kwargs={'pk': self.ca_user1.pk})
        self.url_account2 = reverse(
            'api:coinaccount-detail',
            kwargs={'pk': self.ca_user2.pk})

        # self.url_list_create = reverse('api:transaction-list')
        # self.url_detail = reverse(
        #     'api:transaction-detail',
        #     kwargs={'pk': '1'})

    def test_create(self):
        self.ca_user1.balance = 1
        self.ca_user1.save()
        self.client.force_authenticate(self.testUser1)
        post = {
            'origin': self.url_account1,
            'coin_type': self.url_coin,
            'destination': self.url_account2,
            'ammount': 1
        }
        response = self.client.post(self.url_list_create, post)
        self.assertEquals(response.status_code, 201)

    def test_nobalance(self):
        """If origin has no founds, the transaction must not take place."""
        self.ca_user1.balance = 0
        self.ca_user1.save()
        self.client.force_authenticate(self.testUser1)
        post = {
            'origin': self.url_account1,
            'coin_type': self.url_coin,
            'destination': self.url_account2,
            'ammount': 1
        }
        response = self.client.post(self.url_list_create, post)
        self.assertEquals(response.status_code, 400)

    def test_create_other_user(self):
        """If the transaction is started by another user, it must not be accepted."""
        self.client.force_authenticate(self.testUser2)
        post = {
            'origin': self.url_account1,
            'coin_type': self.url_coin,
            'destination': self.url_account2,
            'ammount': 1
        }
        response = self.client.post(self.url_list_create, post)
        self.assertEquals(response.status_code, 400)
