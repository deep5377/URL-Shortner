from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


def setup_function() -> None:
	Base.metadata.drop_all(bind=engine)
	Base.metadata.create_all(bind=engine)


client = TestClient(app)


def test_create_redirect_and_analytics() -> None:
	response = client.post("/api/v1/urls", json={"url": "https://example.com/docs"})
	assert response.status_code == 201
	code = response.json()["short_code"]

	redirect = client.get(f"/{code}", follow_redirects=False)
	assert redirect.status_code == 307
	assert redirect.headers["location"] == "https://example.com/docs"
	assert client.get(f"/api/v1/urls/{code}/analytics").json()["click_count"] == 1


def test_rejects_unsafe_url_and_expired_url() -> None:
	assert client.post("/api/v1/urls", json={"url": "javascript:alert(1)"}).status_code == 422
	response = client.post(
		"/api/v1/urls",
		json={"url": "https://example.com", "expires_at": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()},
	)
	assert response.status_code == 422
