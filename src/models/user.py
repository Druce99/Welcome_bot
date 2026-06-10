from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum as SQLAlchemyEnum, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base
from src.core.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(Text)
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole, values_callable=lambda x: [e.value for e in x]),
        default=UserRole.BUYER,
    )
    funnel_step: Mapped[int] = mapped_column(Integer, default=0)
    subscribed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    funnel_settings: Mapped["FunnelSettings | None"] = relationship(
        "FunnelSettings",
        back_populates="owner",
        cascade="all, delete-orphan",
    )
    leads_as_owner: Mapped[list["Lead"]] = relationship(
        "Lead",
        foreign_keys="Lead.owner_id",
        back_populates="owner",
    )
    leads_as_buyer: Mapped[list["Lead"]] = relationship(
        "Lead",
        foreign_keys="Lead.buyer_id",
        back_populates="buyer",
    )
    scheduled_messages: Mapped[list["ScheduledMessage"]] = relationship(
        "ScheduledMessage",
        back_populates="user",
        cascade="all, delete-orphan",
    )
