from celery_worker import celery_app
from time import sleep

@celery_app.task
def add(a, b):
    for i in range(a, b):
       print(i)
       sleep(1)
    return {"number": a + b}
