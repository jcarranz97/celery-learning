#!/usr/bin/env python
"""Celery tasks related to group1."""
from time import sleep
from celery import shared_task


@shared_task
def multiply(a: int, b: int):
    """Multiply two numbers and return the result.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        dict: The result of the multiplication.
    """
    for i in range(a, b):
        print(i)
        sleep(1)
    return {"number": a * b}
