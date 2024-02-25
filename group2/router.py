#!/usr/bin/env python
"""FastAPI router related to group2."""
from fastapi import APIRouter
from group2.tasks import multiply
from schemas import TaskId

router = APIRouter()


@router.post("/request-multiply/")
async def send_multiply_task(a: int, b: int) -> TaskId:
    """Send a task to multiply two numbers.

    This function sends a task to the Celery worker to multiply two numbers. It
    returns the task ID to the client.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        TaskId: The task ID.
    """
    task = multiply.delay(a, b)
    return TaskId(task_id=task.id)
