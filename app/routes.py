from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AnalyticsResponse, URLCreate, URLResponse
from app.url_service import create_url, disable_url, get_url, resolve_url

router = APIRouter()


@router.post("/api/v1/urls", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def create(payload: URLCreate, request: Request, db: Session = Depends(get_db)) -> URLResponse:
	return create_url(db, payload, str(request.base_url).rstrip("/"))


@router.get("/api/v1/urls/{short_code}", response_model=URLResponse)
def info(short_code: str, request: Request, db: Session = Depends(get_db)) -> URLResponse:
	return get_url(db, short_code, str(request.base_url).rstrip("/"))


@router.get("/api/v1/urls/{short_code}/analytics", response_model=AnalyticsResponse)
def analytics(short_code: str, db: Session = Depends(get_db)) -> AnalyticsResponse:
	record = get_url(db, short_code, "")
	return AnalyticsResponse(short_code=record.short_code, click_count=record.click_count)


@router.delete("/api/v1/urls/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete(short_code: str, db: Session = Depends(get_db)) -> None:
	disable_url(db, short_code)


@router.get("/{short_code}")
def redirect(short_code: str, db: Session = Depends(get_db)) -> RedirectResponse:
	record = resolve_url(db, short_code)
	return RedirectResponse(record.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
