from fastapi import APIRouter
from group2.tasks import multiply

router = APIRouter()


@router.get("/request-multiply/")
async def send_multiply_task(a: int, b: int):
    task = multiply.delay(a, b)
    return {"task_id": task.id}
