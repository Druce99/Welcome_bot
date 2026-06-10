from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class FunnelSettingsCreate(BaseModel):
    owner_id: int
    channel_username: str = Field(min_length=2)
    welcome_text: str = Field(min_length=1)
    lead_magnet_file_id: str = Field(min_length=1)
    warm_up_text: str = Field(min_length=1)
    offer_text: str = Field(min_length=1)
    offer_price: str = Field(min_length=1)

    @field_validator("channel_username")
    @classmethod
    def validate_channel_username(cls, value: str) -> str:
        if not value.startswith("@"):
            raise ValueError("Username канала должен начинаться с @")
        return value


class FunnelSettingsUpdate(BaseModel):
    channel_username: str | None = Field(default=None, min_length=2)
    welcome_text: str | None = Field(default=None, min_length=1)
    lead_magnet_file_id: str | None = Field(default=None, min_length=1)
    warm_up_text: str | None = Field(default=None, min_length=1)
    offer_text: str | None = Field(default=None, min_length=1)
    offer_price: str | None = Field(default=None, min_length=1)
    is_active: bool | None = None

    @field_validator("channel_username")
    @classmethod
    def validate_channel_username(cls, value: str | None) -> str | None:
        if value is not None and not value.startswith("@"):
            raise ValueError("Username канала должен начинаться с @")
        return value


class FunnelSettingsRead(BaseModel):
    id: int
    owner_id: int
    channel_username: str
    welcome_text: str
    lead_magnet_file_id: str
    warm_up_text: str
    offer_text: str
    offer_price: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
