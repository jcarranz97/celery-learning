#!/usr/bin/env python
"""Main module for the FastAPI application."""
import asyncio
from typing import Annotated
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import Depends
from celery.result import AsyncResult
from celery_worker import celery_app
from group1.router import router as group1_router
from group2.router import router as group2_router
from auth import get_current_username


app = FastAPI()
app.include_router(group1_router, prefix="/group1")
app.include_router(group2_router, prefix="/group2")


@app.get("/")
def read_root():
    """Hello World endpoint."""
    return {"Hello": "World"}


@app.websocket("/ws/task/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    """Websocket endpoint to get the task result."""
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


@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    """Get the current user.

    This method is mainly for testing the dependency injection. In this case
    the basic auth is used to get the username.
    """
    return {"username": username}
