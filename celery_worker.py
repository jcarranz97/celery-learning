from celery import Celery
from time import sleep
 
celery_app = Celery('tasks', broker='redis://redis/0', backend='redis://redis/0')


@celery_app.task
def add(a, b):
    for i in range(a, b):
        print(i)
        sleep(1)
    return {"number": a + b}
