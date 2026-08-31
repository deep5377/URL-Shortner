from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utcnow() -> datetime:
	return datetime.now(timezone.utc)


class URLRecord(Base):
	__tablename__ = "urls"

	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	short_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
	original_url: Mapped[str] = mapped_column(Text)
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
	expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True)
	click_count: Mapped[int] = mapped_column(Integer, default=0)
