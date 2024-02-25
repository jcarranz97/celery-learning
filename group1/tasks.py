#!/usr/bin/env python
"""Celery tasks related to group2."""
from time import sleep
from celery import shared_task


@shared_task
def add(a: int, b: int):
    """Add two numbers and return the result.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        dict: The result of the addition.
    """
    for i in range(a, b):
        print(i)
        sleep(1)
    return {"number": a + b}
