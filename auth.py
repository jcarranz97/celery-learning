#!/usr/bin/env python3
"""Module that defines the authentication for the API."""
import secrets
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBasic
from fastapi.security.http import HTTPBasicCredentials
from fastapi import HTTPException
from fastapi import status


security = HTTPBasic()

users_fake_db = {
    "stanley": {
        "username": "stanley",
        "password": "swordfish",
        "email": "stanley@gmail.com",
    },
    "jcarranz": {
        "username": "jcarranz",
        "password": "password",
        "email": "Juan@gmail.com",
    },
}


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    """Function to authenticate and get the current username."""
    # This is a very basic implementation of authentication and the users
    # database is just a fake in-memory dictionary.
    if credentials.username not in users_fake_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = \
        users_fake_db[credentials.username]["password"].encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not is_correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
