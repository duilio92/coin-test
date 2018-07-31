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
        related_name='origin_transactions',
        on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        CoinAccount,
        related_name='destination_transactions',
        on_delete=models.CASCADE
    )
    ammount = models.IntegerField()
    coin_type = models.ForeignKey(Coin, on_delete=models.PROTECT)

    def __str__(self):
        return '%s %s %s' % (self.date, self.origin, self.destination)

    # def save(self, *args, **kwargs):
    #     print "recibi llamada a save"
    #     if self.origin.balance - self.ammount < 0:
    #         return  # an account cant debit to a negative balance
    #     # next 4 lines should be atomic
    #     self.origin.balance = self.origin.balance - self.ammount
    #     self.destination.balance = self.destination.balance + self.ammount
    #     self.origin.save()
    #     self.destination.save()
    #     super(Transaction, self).save(*args, **kwargs)
