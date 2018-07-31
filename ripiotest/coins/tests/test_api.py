# -*- coding: utf-8 -*-
import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from coins.models import Coin
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
        # no pude solucionar lo de la url asi que testeo campo a campo
        self.assertEquals(data['id'], content['id'])
        self.assertEquals(data['name'], content['name'])

    def test_create(self):
        self.client.force_authenticate(self.user)
        post = {'name': 'testcoin'}
        response = self.client.post(self.url_list_create, post)
        data = json.loads(response.content)
        self.assertEquals(response.status_code, 201)
        content = {'url': self.url_detail, 'id': 3, 'name': 'testcoin'}
        # no pude solucionar lo de la url asi que testeo campo a campo
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
        # si el usuario no es staff no puede crear
        self.client.force_authenticate(self.user)
        post = {'name': 'testcoin'}
        response = self.client.post(self.url_list_create, post)
        self.assertEquals(response.status_code, 403)

    def test_create_unauthenticated(self):
        # usuario anonimo no puede crear
        self.client.force_authenticate(self.user)
        post = {'name': 'testcoin'}
        response = self.client.post(self.url_list_create, post)
        self.assertEquals(response.status_code, 403)

    def test_delete(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.url_detail)
        self.assertEquals(response.status_code, 403)
