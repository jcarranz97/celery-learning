from fastapi import APIRouter
from group2.tasks import multiply
from schemas import TaskId

router = APIRouter()


@router.post("/request-multiply/")
async def send_multiply_task(a: int, b: int) -> TaskId:
    task = multiply.delay(a, b)
    return TaskId(task_id=task.id)
