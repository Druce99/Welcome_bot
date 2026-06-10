from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class FunnelSettings(Base):
    __tablename__ = "funnel_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), unique=True)
    channel_username: Mapped[str] = mapped_column(Text)
    welcome_text: Mapped[str] = mapped_column(Text)
    lead_magnet_file_id: Mapped[str | None] = mapped_column(Text)
    lead_magnet_text: Mapped[str | None] = mapped_column(Text)
    warm_up_text: Mapped[str] = mapped_column(Text)
    offer_text: Mapped[str] = mapped_column(Text)
    offer_price: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    owner: Mapped["User"] = relationship("User", back_populates="funnel_settings")
