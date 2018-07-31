from celery import Celery
from celery_once import QueueOnce
from time import sleep
#from transactions.models import Transaction
celery = Celery(
    'tasks',
    backend='redis://127.0.0.1:6379/0',
    broker='pyamqp://guest@localhost//')
# celery.conf.ONCE = {
#     'backend': 'celery_once.backends.Redis',
#     'settings': {
#         'url': 'redis://127.0.0.1:6379/0',
#         'default_timeout': 60 * 60
#     }
# }


@celery.task
def add(x, y):
    return x + y


@celery.task
def slow_task():
    sleep(30)
    return "Done!"


# @celery.task(base=QueueOnce)
# def create_transaction(transaction):
#     Transaction.objects.create(transaction)
