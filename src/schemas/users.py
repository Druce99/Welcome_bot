from datetime import datetime

from pydantic import BaseModel, Field

from src.core.enums import UserRole


class UserCreate(BaseModel):
    id: int
    username: str | None = None
    role: UserRole = UserRole.BUYER


class UserUpdate(BaseModel):
    funnel_step: int | None = Field(default=None, ge=0)
    role: UserRole | None = None


class UserRead(BaseModel):
    id: int
    username: str | None
    role: UserRole
    funnel_step: int
    subscribed_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
