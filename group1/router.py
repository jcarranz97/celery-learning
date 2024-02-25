#!/usr/bin/env python
"""FastAPI router related to group1."""
from fastapi import APIRouter
from fastapi import Depends
from group1.tasks import add
from schemas import TaskId
from auth import get_current_username

router = APIRouter()


@router.post("/request-add")
async def send_add_task(a: int, b: int) -> TaskId:
    """Send a task to add two numbers.

    This function sends a task to the Celery worker to add two numbers. It
    returns the task ID to the client.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        TaskId: The task ID.
    """
    task = add.delay(a, b)
    return TaskId(task_id=task.id)


# This route is protected by the get_current_username dependency
# This means that the client must send a valid token in the Authorization
# header to access this route, and the username of the token will be
# available in the get_current_username function, but it won't be used
# in this route.
@router.get("/get-result", dependencies=[Depends(get_current_username)])
async def get_task_result(task_id: str):
    """Get the result of a task.

    This function returns the result of a task given its ID.

    Args:
        task_id (str): The ID of the task.

    Returns:
        dict: The status of the task and its result.
    """
    task = add.AsyncResult(task_id)
    if not task.ready():
        return {"status": "PENDING"}
    return {"status": "SUCCESS", "result": task.get()}
