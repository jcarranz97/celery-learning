import asyncio
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from celery.result import AsyncResult
from fastapi import status
from celery_worker import celery_app
from group1.router import router as group1_router
from group2.router import router as group2_router
from auth import fake_users_db
from auth import UserInDB
from auth import get_current_active_user
from auth import User
from typing import Annotated
from auth import authenticate_user
from auth import Token
from auth import create_access_token


app = FastAPI()
app.include_router(group1_router, prefix="/group1")
app.include_router(group2_router, prefix="/group2")


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


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
