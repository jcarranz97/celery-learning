from fastapi import FastAPI
from fastapi import WebSocket
from celery_worker import celery_app
from tasks1 import add
from celery.result import AsyncResult
import asyncio

import time

app = FastAPI()


@app.get("/process")
async def process_endpoint(a: int, b: int):
    task = add.delay(a, b)
    return {"task_id": task.id}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.websocket("/ws/task/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()

    # Get the task result asynchronously
    result = AsyncResult(task_id, app=celery_app)

    while not result.ready():
        await websocket.send_text("Processing...")
        await asyncio.sleep(1)

    # If result is successful, send the state and result
    if result.successful():
        await websocket.send_text(f"Task {task_id} succeeded: {result.result}")
    else:
        await websocket.send_text(f"Task {task_id} failed: {result.result}")
