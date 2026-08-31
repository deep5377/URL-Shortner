from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_greenfield_workflow_reaches_release_ready() -> None:
	response = client.post("/api/v1/workflows", json={"requirement": "Build a URL shortening API"})
	assert response.status_code == 201
	workflow = response.json()
	assert workflow["status"] == "RELEASE_READY"
	assert workflow["test_results"]["passed"] is True
	assert workflow["events"]


def test_brownfield_requires_approval() -> None:
	response = client.post("/api/v1/workflows", json={"requirement": "Add expiration support to existing URLs"})
	workflow = response.json()
	assert workflow["status"] == "AWAITING_APPROVAL"
	approved = client.post(f"/api/v1/workflows/{workflow['workflow_id']}/approve", json={"approver": "reviewer"})
	assert approved.json()["status"] == "RELEASE_READY"


def test_ambiguous_workflow_safe_stops() -> None:
	response = client.post("/api/v1/workflows", json={"requirement": "Make popular URLs faster"})
	assert response.json()["status"] == "SAFE_STOP"


def test_destructive_workflow_requires_high_risk_approval() -> None:
	response = client.post("/api/v1/workflows", json={"requirement": "Permanently delete all expired URLs"})
	workflow = response.json()
	assert workflow["risk_level"] == "HIGH"
	assert workflow["status"] == "AWAITING_APPROVAL"


def test_health_history_and_clarification_endpoints() -> None:
	assert client.get("/health").json() == {"status": "ok"}
	ambiguous = client.post("/api/v1/workflows", json={"requirement": "Make popular URLs faster"}).json()
	clarified = client.post(
		f"/api/v1/workflows/{ambiguous['workflow_id']}/clarify",
		json={"clarification": "Popular means over 100 redirects per hour; target P95 latency is under 50ms; caching is allowed."},
	).json()
	assert clarified["requirement_version"] == 2
	assert clarified["status"] in {"RELEASE_READY", "AWAITING_APPROVAL"}
	assert any(event["action"] == "clarification_received" for event in clarified["events"])
	assert any(item["workflow_id"] == clarified["workflow_id"] for item in client.get("/api/v1/workflows").json())


def test_rollback_restores_checkpoint_and_safe_stops() -> None:
	workflow = client.post("/api/v1/workflows", json={"requirement": "Build a URL shortening API"}).json()
	rolled_back = client.post(f"/api/v1/workflows/{workflow['workflow_id']}/rollback").json()
	assert rolled_back["status"] == "SAFE_STOP"
	assert rolled_back["rollback_count"] == 1
	assert rolled_back["current_stage"] == "GOVERNANCE"
	assert rolled_back["events"][-1]["action"] == "rollback_workflow"
