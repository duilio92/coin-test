from celery import Celery
from celery_once import QueueOnce
from time import sleep

celery = Celery('tasks', broker='amqp://localhost')
celery.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': 'redis://localhost:6379/0',
        'default_timeout': 60 * 60
    }
}


@celery.task
def add(x, y):
    return x + y


@celery.task(base=QueueOnce)
def slow_task():
    sleep(30)
    return "Done!"
