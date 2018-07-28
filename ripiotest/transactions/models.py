# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from coins.models import CoinAccount, Coin


class Transaction(models.Model):
    """A transference in a given coin, from one user to another."""

    date = models.DateTimeField(default=timezone.now, editable=False)
    origin = models.ForeignKey(
        CoinAccount,
        related_name='origin',
        on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        CoinAccount,
        related_name='destiny',
        on_delete=models.CASCADE
    )
    ammount = models.IntegerField()
    coin_type = models.ForeignKey(Coin, on_delete=models.PROTECT)

    def __str__(self):
        return '%s %s %s' % (self.date, self.origin, self.destiny)
