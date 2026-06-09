from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: dict = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    error: ErrorDetail


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    created_at: datetime


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ProjectResponse(BaseModel):
    id: UUID
    team_id: UUID
    name: str
    description: str | None
    status: Literal["active", "archived"]
    created_by: UUID
    created_at: datetime
    updated_at: datetime


class ProjectCreate(BaseModel):
    team_id: UUID
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class TaskResponse(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    description: str | None
    status: Literal["todo", "in_progress", "done"]
    assignee_id: UUID | None
    created_by: UUID
    position: int
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    description: str | None = None
    status: Literal["todo", "in_progress", "done"] = "todo"
    assignee_id: UUID | None = None
    position: int = 0


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    description: str | None = None
    status: Literal["todo", "in_progress", "done"] | None = None
    assignee_id: UUID | None = None
    position: int | None = None


class CommentResponse(BaseModel):
    id: UUID
    task_id: UUID
    author_id: UUID
    author_name: str
    body: str
    created_at: datetime
    updated_at: datetime


class CommentCreate(BaseModel):
    body: str = Field(min_length=1)