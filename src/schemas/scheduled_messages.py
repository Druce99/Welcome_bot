from datetime import datetime

from pydantic import BaseModel

from src.core.enums import MessageType


class ScheduledMessageCreate(BaseModel):
    user_id: int
    message_type: MessageType
    send_at: datetime


class ScheduledMessageRead(BaseModel):
    id: int
    user_id: int
    message_type: MessageType
    send_at: datetime
    is_sent: bool
    created_at: datetime

    model_config = {"from_attributes": True}
