#!/usr/bin/env python3
"""Module to define generic schemas for the API."""
from pydantic import BaseModel


class TaskId(BaseModel):
    """Schema for a task id."""

    task_id: str
