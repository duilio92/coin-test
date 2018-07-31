from __future__ import absolute_import
from celery import Celery
from celery_once import QueueOnce
from time import sleep
from ripiotest.settings import local as settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ripiotest.settings.local')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ripiotest.settings.local')
# from django.conf import settings

# backend='redis://127.0.0.1:6379/0',
celery = Celery(
    'tasks',
    backend='redis://127.0.0.1:6379/0',
    broker='pyamqp://guest@localhost//')
celery.autodiscover_tasks(lambda: settings.INSTALLED_APPS) 
# celery.conf.ONCE = {
#     'backend': 'celery_once.backends.Redis',
#     'settings': {
#         'url': 'redis://127.0.0.1:6379/0',
#         'default_timeout': 60 * 60
#     }
# }


# @celery.task #(base=QueueOnce)
# def slow_task():
#     from transactions.models import Transaction
#     t = Transaction()
#     return "Done!"


# @celery.task #(base=QueueOnce)
# def add():
#     return 4 + 5

@celery.task #(base=QueueOnce)
def create_transaction():
    from transactions.models import Transaction
    sleep(30)
    return "Done!"
