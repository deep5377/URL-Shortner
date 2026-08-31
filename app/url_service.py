import secrets
import string
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import URLRecord
from app.schemas import URLCreate, URLResponse

ALPHABET = string.ascii_letters + string.digits


def _is_expired(record: URLRecord) -> bool:
	return record.expires_at is not None and record.expires_at <= datetime.now(timezone.utc)


def _response(record: URLRecord, base_url: str) -> URLResponse:
	return URLResponse(
		short_code=record.short_code,
		short_url=f"{base_url.rstrip('/')}/{record.short_code}",
		original_url=record.original_url,
		expires_at=record.expires_at,
		is_active=record.is_active,
		click_count=record.click_count,
	)


def create_url(db: Session, payload: URLCreate, base_url: str) -> URLResponse:
	if payload.expires_at and payload.expires_at <= datetime.now(timezone.utc):
		raise HTTPException(status_code=422, detail="expires_at must be in the future")
	for _ in range(5):
		code = "".join(secrets.choice(ALPHABET) for _ in range(6))
		if db.scalar(select(URLRecord).where(URLRecord.short_code == code)) is None:
			record = URLRecord(short_code=code, original_url=str(payload.url), expires_at=payload.expires_at)
			db.add(record)
			db.commit()
			db.refresh(record)
			return _response(record, base_url)
	raise HTTPException(status_code=503, detail="could not allocate a unique short code")


def get_url(db: Session, short_code: str, base_url: str) -> URLResponse:
	record = db.scalar(select(URLRecord).where(URLRecord.short_code == short_code))
	if record is None:
		raise HTTPException(status_code=404, detail="short URL not found")
	return _response(record, base_url)


def resolve_url(db: Session, short_code: str) -> URLRecord:
	record = db.scalar(select(URLRecord).where(URLRecord.short_code == short_code))
	if record is None or not record.is_active:
		raise HTTPException(status_code=404, detail="short URL not found")
	if _is_expired(record):
		raise HTTPException(status_code=410, detail="short URL has expired")
	record.click_count += 1
	db.commit()
	return record


def disable_url(db: Session, short_code: str) -> None:
	record = db.scalar(select(URLRecord).where(URLRecord.short_code == short_code))
	if record is None:
		raise HTTPException(status_code=404, detail="short URL not found")
	record.is_active = False
	db.commit()
