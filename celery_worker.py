#!/usr/bin/env python
"""Celery worker module."""
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis/0",
    backend="redis://redis/0",
    include=[
        "group1.tasks",
        "group2.tasks",
    ],
)
