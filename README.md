# Agentic URL Shortener

This repository is a working prototype for the Agentic Software Engineering System assignment. It combines a URL shortener product with a governed requirement-to-release workflow.

## Prerequisites

- Python 3.12+.
- Node.js 18+ and npm for the frontend.
- Git for source-control demonstrations.
- An OpenAI API key only when enabling LLM assessment.

## Backend setup

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Backend URLs:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

SQLite creates `url_shortener.db` on startup. Override `DATABASE_URL` in `.env` for another SQLAlchemy-compatible database.

## Environment variables

The root `.env` file is ignored by Git. Start from `.env.example`:

```env
OPENAI_API_KEY=sk-your-key-here
USE_LLM=false
OPENAI_MODEL=gpt-4o-mini
DATABASE_URL=sqlite:///./url_shortener.db
```

Set `USE_LLM=true` only when a valid `OPENAI_API_KEY` is configured. The LLM returns a Pydantic-validated requirement assessment. Disabled, unavailable, or invalid LLM output falls back to deterministic assessment and is recorded in workflow events.

## Frontend setup

Keep the backend running, then open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The frontend uses `frontend/.env` and defaults to:

```env
VITE_API_BASE_URL=http://localhost:8000
```

The control center uses real health, workflow, approval, clarification, rollback, metrics, and URL endpoints. It does not simulate workflow progress. API status is based on `GET /health`, and URL creation is disabled while the backend is offline.

### Windows one-command start

After the backend environment and frontend dependencies are installed, double-click `start.bat` from the repository root. It opens separate terminals for:

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173`

The script expects `.venv\Scripts\python.exe` and `frontend\node_modules` to exist. Close both terminal windows to stop the services.

## What the system does

1. Accepts a natural-language requirement.
2. Creates a structured requirement assessment.
3. Detects ambiguity and assigns risk.
4. Performs architecture and brownfield impact analysis.
5. Creates dependency-aware tasks.
6. Runs the LangGraph workflow.
7. Executes deterministic validation.
8. Requests approval for medium/high-risk work.
9. Safe-stops ambiguous, unsafe, or exhausted work.
10. Records events, decisions, validation evidence, and outcomes.

The React application renders backend state; it never decides risk, approval, validation status, retry eligibility, safe-stop, or release readiness.

## API examples

```powershell
curl -X POST http://localhost:8000/api/v1/urls -H "Content-Type: application/json" -d '{"url":"https://example.com"}'
curl -X POST http://localhost:8000/api/v1/workflows -H "Content-Type: application/json" -d '{"requirement":"Build a URL shortening API"}'
```

Workflow endpoints include:

- `POST /api/v1/workflows`
- `GET /api/v1/workflows`
- `GET /api/v1/workflows/{workflow_id}`
- `GET /api/v1/workflows/{workflow_id}/events`
- `POST /api/v1/workflows/{workflow_id}/approve`
- `POST /api/v1/workflows/{workflow_id}/reject`
- `POST /api/v1/workflows/{workflow_id}/clarify`
- `POST /api/v1/workflows/{workflow_id}/rollback`
- `GET /api/v1/metrics`

## Testing approach

Unit and integration tests cover URL validation, short-code creation, redirect behavior, analytics, expiration, requirement assessment, ambiguity detection, risk classification, approval, safe-stop, health, history, clarification/replanning, and rollback.

Run the complete backend suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Run quality and security gates:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m bandit -r app orchestrator -q
.\.venv\Scripts\python.exe -m pip_audit
```

Build the frontend:

```powershell
cd frontend
npm run build
```

The workflow uses pytest evidence for release gating. Bandit and pip-audit are repository quality gates; the prototype security policy also records input validation, secret configuration, and safe URL scheme checks.

## Demonstration scenarios

Scenario definitions are in `data/scenarios.json`:

- **Greenfield:** Build a URL shortening API. Expected path: validation to `RELEASE_READY`.
- **Brownfield:** Add expiration support. Expected path: impact analysis and approval.
- **Ambiguous:** Make popular URLs faster. Expected path: ambiguity detection and `SAFE_STOP`.
- **High risk:** Permanently delete expired URLs. Expected path: high-risk approval.
- **Requirement change:** Add administrator recovery for expired URLs. Expected path: version increment and re-planning.

The URL examples in `data/sample_urls.json` cover normal links, future expiration, expired links, and disabled-link behavior.

## Docker

```powershell
docker build -t agentic-url-shortener .
docker run -p 8000:8000 agentic-url-shortener
```

## Trade-offs

- SQLite keeps setup reproducible and infrastructure-free, but is not the right production database for high concurrency.
- A single lightweight LLM keeps cost and debugging manageable; role specialization comes from prompts, schemas, state, tools, and policies.
- Polling is simpler than WebSockets for this prototype.
- Workflow state is explicit and auditable, but currently held in process memory.
- The implementation agent produces a changed-file manifest rather than applying generated patches, which limits automation risk but means the prototype does not modify a repository from a requirement.
- Aggregate click counts are simple and privacy-conscious, but do not provide a full event analytics history.

## Limitations

- Workflow state is lost when the process restarts.
- Execution is synchronous rather than worker-backed and asynchronous.
- Architecture and Risk are represented as synchronized state outputs, not independently scheduled worker processes.
- Retry counters and safe-stop routing exist, but a complete diagnosis, corrective patch, and retry loop is not implemented.
- Rollback restores workflow state, not repository source files.
- Security scanner execution is primarily a repository/CI quality gate rather than a full per-workflow scanner adapter.
- Metrics do not yet provide full MTTR, failure-rate history, token cost, or production latency telemetry.
- Requirement re-planning increments the version but does not yet provide complete task invalidation mapping.
- Authentication, RBAC, rate limiting, migrations, distributed workers, and enterprise observability are out of scope.

More detail is available in [docs/PROJECT_EXPLANATION.md](docs/PROJECT_EXPLANATION.md), [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), and [docs/TEST_PLAN.md](docs/TEST_PLAN.md).
