from __future__ import absolute_import
from celery import Celery
from ripiotest.settings import local as settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ripiotest.settings.local')
os.environ.setdefault('CELERY_CONFIG_MODULE', 'ripiotest.settings.celeryconfig')

celery = Celery()

celery.config_from_envvar('CELERY_CONFIG_MODULE')
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@celery.task
def create_transaction(ammount, origin, destination, coin_type):
    from transactions.models import Transaction
    from coins.models import Coin, CoinAccount
    t = Transaction()
    t.ammount = ammount
    t.coin_type = Coin.objects.get(pk=coin_type)
    t.origin = CoinAccount.objects.get(pk=origin)
    t.destination = CoinAccount.objects.get(pk=destination)
    t.save()
    return t.pk
