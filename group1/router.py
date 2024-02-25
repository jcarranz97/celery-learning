from fastapi import APIRouter
from group1.tasks import add

router = APIRouter()


@router.get("/request-add")
async def send_add_task(a: int, b: int):
    task = add.delay(a, b)
    return {"task_id": task.id}
