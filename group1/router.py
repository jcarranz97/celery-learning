from fastapi import APIRouter
from group1.tasks import add
from schemas import TaskId

router = APIRouter()


@router.get("/request-add")
async def send_add_task(a: int, b: int) -> TaskId:
    task = add.delay(a, b)
    return TaskId(task_id=task.id)
