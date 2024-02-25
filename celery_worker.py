from celery import Celery
from time import sleep
 
celery_app = Celery(
    'tasks',
    broker='redis://redis/0',
    backend='redis://redis/0',
    include=['tasks1']
)
