# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Coin(models.Model):
    name = models.CharField(max_length=30)


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    pubkey = models.CharField(max_length=100, blank=True)  # REVISAR
    privkey = models.CharField(max_length=100, blank=True)  # REVISAR


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        a = Account.objects.create(user=instance)
        a.pubkey = uuid.uuid4().hex
        a.privkey = uuid.uuid4().hex


@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()


class CoinAccount(models.Model):
    balance = models.IntegerField(default=0)
    main_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    coin_type = models.ForeignKey(Coin, on_delete=models.PROTECT)


class Transaction(models.Model):
    date = models.DateTimeField()
    origin = models.ForeignKey(
        Account,
        related_name='origin',
        on_delete=models.CASCADE
    )
    destiny = models.ForeignKey(
        Account,
        related_name='destiny',
        on_delete=models.CASCADE
    )
    value = models.IntegerField()
    coin_type = models.ForeignKey(Coin, on_delete=models.PROTECT)
