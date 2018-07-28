# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from coins.models import Account, Coin


class Transaction(models.Model):
    """A transference in a given coin, from one user to another."""

    date = models.DateTimeField()
    origin = models.ForeignKey(
        Account,
        related_name='origin',
        on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Account,
        related_name='destiny',
        on_delete=models.CASCADE
    )
    ammount = models.IntegerField()
    coin_type = models.ForeignKey(Coin, on_delete=models.PROTECT)

    def __str__(self):
        return '%s %s %s' % (self.date, self.origin, self.destiny)
