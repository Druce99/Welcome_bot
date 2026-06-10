from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    buyer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    buyer_username: Mapped[str | None] = mapped_column(Text)
    buyer_contact: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    owner: Mapped["User"] = relationship(
        "User", foreign_keys=[owner_id], back_populates="leads_as_owner"
    )
    buyer: Mapped["User"] = relationship(
        "User", foreign_keys=[buyer_id], back_populates="leads_as_buyer"
    )
