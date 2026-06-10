from datetime import datetime

from pydantic import BaseModel, Field


class LeadCreate(BaseModel):
    owner_id: int
    buyer_id: int
    buyer_username: str | None = None
    buyer_contact: str = Field(min_length=1)


class LeadRead(BaseModel):
    id: int
    owner_id: int
    buyer_id: int
    buyer_username: str | None
    buyer_contact: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
