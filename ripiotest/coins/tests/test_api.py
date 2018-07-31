# -*- coding: utf-8 -*-
import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from coins.models import Coin, Account, CoinAccount
from django.contrib.auth.models import User


class CoinAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testing2",
            password="t3st1ng!!",
            is_staff=True)
        self.client = APIClient()

        Coin.objects.get_or_create(name="duicoin")
        Coin.objects.get_or_create(name="bitcoin")
        self.url_list_create = reverse('api:coin-list')
        self.url_detail = reverse('api:coin-detail', kwargs={'name': 'duicoin'})

    def test_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url_list_create)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "duicoin")
        self.assertContains(response, "bitcoin")

    def test_detail(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url_detail)
        data = json.loads(response.content)
        content = {'url': self.url_detail, 'id': 1, 'name': 'duicoin'}
        # url gives error when comparing content, so will compare all others field
        self.assertEquals(data['id'], content['id'])
        self.assertEquals(data['name'], content['name'])

    def test_create(self):
        self.client.force_authenticate(self.user)
        post = {'name': 'testcoin'}
        response = self.client.post(self.url_list_create, post)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 201)
        content = {'url': self.url_detail, 'id': 3, 'name': 'testcoin'}
        # url gives error when comparing content, so will compare all others field
        self.assertEquals(data['id'], content['id'])
        self.assertEquals(data['name'], content['name'])
        self.assertEquals(Coin.objects.count(), 3)

    def test_delete(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url_detail)
        self.assertEquals(response.status_code, 204)
        self.assertEquals(Coin.objects.count(), 1)


class CoinApiTestsPermissions(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testing",
            password="t3st1ng!!"
        )
        #by deffault the user isnt staff

        self.client = APIClient()

        Coin.objects.get_or_create(name="duicoin")
        Coin.objects.get_or_create(name="bitcoin")
        self.url_list_create = reverse('api:coin-list')
        self.url_detail = reverse('api:coin-detail', kwargs={'name': 'duicoin'})

    def test_create(self):
        # if user is not staffed he must not be allwoed to create.
        self.client.force_authenticate(self.user)
        post = {'name': 'testcoin'}
        response = self.client.post(self.url_list_create, post)
        self.assertEquals(response.status_code, 403)

    def test_create_unauthenticated(self):
        # anonymus user must not be allowed to create.
        self.client.force_authenticate(self.user)
        post = {'name': 'testcoin'}
        response = self.client.post(self.url_list_create, post)
        self.assertEquals(response.status_code, 403)

    def test_delete(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url_detail)
        self.assertEquals(response.status_code, 403)


class AccountAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testing2",
            password="t3st1ng!!",
            is_staff=True)
        self.client = APIClient()
        # create test users to create accounts
        User.objects.create(username="user1", password="t3stfirst")
        User.objects.create(username="user2", password="t3stsecond")
        account,created = Account.objects.get_or_create(user__username="user1")
        Account.objects.get_or_create(user__username="user2")
        self.url_list_create = reverse('api:account-list')
        self.url_detail = reverse('api:account-detail', kwargs={'pk': account.id})

    def test_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url_list_create)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "user1 account")
        self.assertContains(response, "user2 account")

    # def test_detail(self):
    # def test_update_ammount(self):
    #     #TODO
    #     #el monto no deberia poder ser negativo incluso si lo intento
    # def test_create(self):
    # def test_delete(self):


class CoinAccountAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testing2",
            password="t3st1ng!!",
            is_staff=True)
        self.client = APIClient()
        # create test users to create accounts
        self.testUser1 = User.objects.create(username="user1", password="t3stfirst")
        self.testUser2 =User.objects.create(username="user2", password="t3stsecond")
        self.url_list_create = reverse('api:coinaccount-list')

        self.coin, created = Coin.objects.get_or_create(name="bitcoin")
        coin2, created = Coin.objects.get_or_create(name="ether")

        CoinAccount.objects.create(
            coin_type=self.coin,
            main_account=self.testUser1.account)
        CoinAccount.objects.create(
            coin_type=coin2,
            main_account=self.testUser2.account)
        
        self.url_coin = reverse('api:coin-detail', kwargs={'name': self.coin.name})
        self.url_user_main_account = reverse('api:account-detail', kwargs={'pk': self.user.id})
        
        #self.url_detail = reverse('api:coinaccount-detail', kwargs={'pk': account.id})

    def test_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url_list_create)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "user1 bitcoin")
        self.assertContains(response, "user2 ether")

    def test_create(self):
        self.client.force_authenticate(self.user)
        post = {"coin_type": self.url_coin, "main_account": self.url_user_main_account}
        response = self.client.post(self.url_list_create, post)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(CoinAccount.objects.count(), 3)
        
    def test_create_other_user(self):
        # if an user tries to open an account for other user, it must be dennied
        self.client.force_authenticate(self.testUser2)
        post = {"coin_type": self.url_coin, "main_account": self.url_user_main_account}
        response = self.client.post(self.url_list_create, post)
        data = json.loads(response.content)
        self.assertNotEquals(response.status_code, 201)
        self.assertEquals(CoinAccount.objects.count(), 3)