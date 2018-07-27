# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Coin, CoinAccount, Account

admin.site.register(Coin)
admin.site.register(CoinAccount)
admin.site.register(Account)
