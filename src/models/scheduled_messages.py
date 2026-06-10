from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Enum as SQLAlchemyEnum, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base
from src.core.enums import MessageType


class ScheduledMessage(Base):
    __tablename__ = "scheduled_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    message_type: Mapped[MessageType] = mapped_column(
        SQLAlchemyEnum(MessageType, values_callable=lambda x: [e.value for e in x])
    )
    send_at: Mapped[datetime] = mapped_column(DateTime)
    is_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="scheduled_messages")
