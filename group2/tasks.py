from celery import shared_task
from time import sleep


@shared_task
def multiply(a, b):
    for i in range(a, b):
        print(i)
        sleep(1)
    return {"number": a * b}
