from fastapi import APIRouter
from group1.tasks import add
from schemas import TaskId

router = APIRouter()


@router.post("/request-add")
async def send_add_task(a: int, b: int) -> TaskId:
    task = add.delay(a, b)
    return TaskId(task_id=task.id)


@router.get("/get-result")
async def get_task_result(task_id: str):
    task = add.AsyncResult(task_id)
    if not task.ready():
        return {"status": "PENDING"}
    return {"status": "SUCCESS", "result": task.get()}
