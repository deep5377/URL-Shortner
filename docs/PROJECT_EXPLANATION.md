# Agentic URL Shortener
## Complete Project Explanation

**Project type:** Agentic Software Engineering System prototype
**Purpose:** Transform a natural-language software requirement into a structured, reviewable, validated, and governed engineering outcome.
**Primary workload:** URL shortener service
**Audience:** Engineering interview demonstration and prototype review

---

## 1. Executive Summary

This project demonstrates a controlled AI-assisted software development lifecycle. A user submits a software requirement, for example:

```text
Add expiration support to existing shortened URLs.
```

The system then:

1. Preserves the original requirement.
2. Normalizes and classifies the requirement.
3. Detects ambiguity and missing information.
4. Assigns risk.
5. Performs architecture and impact analysis.
6. Decomposes the work into dependent engineering tasks.
7. Executes a LangGraph workflow.
8. Runs deterministic validation tools.
9. Pauses for human approval when policy requires it.
10. Records decisions, events, evidence, and outcomes.
11. Produces a release-ready or safe-stop result.

The central engineering principle is:

> Agents may perform meaningful work, but deterministic tools and policy gates control what can be released. Humans retain final authority for high-impact changes.

---

## 2. What Was Built

### Backend

- FastAPI REST application.
- SQLite persistence through SQLAlchemy.
- URL creation and short-code generation.
- Short URL redirect handling.
- URL expiration support.
- Aggregate redirect analytics.
- URL disablement.
- Input validation using Pydantic.
- CORS support for the Vite development server.
- Health endpoint for real frontend connectivity status.

### Agentic orchestration

- LangGraph state graph.
- Requirement assessment agent.
- Architecture and impact analysis agent.
- Planning and task decomposition agent.
- Implementation manifest agent.
- Deterministic test and security validation tools.
- Policy-based risk and approval controls.
- Retry limit and safe-stop behavior.
- Workflow event and decision history.
- Workflow history and detail APIs.
- Ambiguous requirement clarification and re-planning.
- Pre-execution workflow checkpoint rollback.

### LLM integration

- Centralized OpenAI service boundary.
- Structured Pydantic output.
- Optional OpenAI execution.
- Deterministic fallback when the LLM is disabled, unavailable, times out, or returns invalid output.
- LLM usage and fallback are recorded in workflow events.

### Frontend

- React and TypeScript application built with Vite.
- Framer Motion for restrained state and event transitions.
- Dark engineering control-center visual design.
- Dashboard with real workflow metrics.
- New Run screen with demonstration scenarios.
- Workflow history list.
- Workflow detail screen.
- Real workflow graph state rendering.
- Requirement analysis and confidence display.
- Task dependencies and validation gates.
- Approval and rejection controls.
- Ambiguity clarification form.
- Audit event timeline.
- URL shortener product demo.
- Live backend health indicator.
- Responsive desktop, tablet, and mobile layout.

---

## 3. Architecture

```text
React / Vite Frontend
          |
          | Typed fetch API
          v
FastAPI Application
     |              |
     |              +--> Workflow Control API
     |                         |
     |                         v
     |                   LangGraph State Graph
     |                         |
     |              +----------+----------+
     |              |                     |
     v              v                     v
URL Service    Requirement Agent    Policy / Gates
     |              |                     |
     v              v                     v
SQLAlchemy    Assessment State       Deterministic Tools
     |                                    |
     v                                    v
SQLite                         pytest / Security Evidence
```

### Backend modules

| File | Responsibility |
| --- | --- |
| `app/main.py` | FastAPI application, startup, health, and CORS configuration |
| `app/database.py` | SQLAlchemy engine, session dependency, table creation |
| `app/models.py` | URL database model |
| `app/schemas.py` | API request and response validation models |
| `app/url_service.py` | URL business logic, expiration, redirects, and collision handling |
| `app/routes.py` | URL API routes and redirect route |
| `orchestrator/state.py` | Shared workflow state, assessment, task, and event schemas |
| `orchestrator/agents.py` | Requirement, architecture, planning, and implementation agents |
| `orchestrator/graph.py` | LangGraph construction, routing, workflow APIs, approval, clarification, rollback, and metrics |
| `orchestrator/policies.py` | Risk classification, approval policy, and release gate |
| `orchestrator/tools.py` | Deterministic pytest execution, validation caching, and security checks |
| `orchestrator/llm_service.py` | Centralized optional OpenAI structured-output service |

### Frontend modules

| File | Responsibility |
| --- | --- |
| `frontend/src/App.tsx` | Application state, navigation, polling, health, and actions |
| `frontend/src/api.ts` | Centralized typed FastAPI client |
| `frontend/src/types.ts` | TypeScript representations of backend contracts |
| `frontend/src/styles.css` | Existing dark control-center visual system and responsive layout |
| `components/Sidebar.tsx` | Main navigation |
| `components/Dashboard.tsx` | Overview, metrics, latest workflow, analysis, and task plan |
| `components/RequirementForm.tsx` | Requirement submission and demo scenarios |
| `components/WorkflowList.tsx` | Real workflow history |
| `components/WorkflowDetail.tsx` | Workflow facts, graph, gates, clarification, tasks, and events |
| `components/WorkflowGraph.tsx` | Backend-driven workflow node and connector visualization |
| `components/WorkflowNode.tsx` | Individual workflow node state presentation |
| `components/ApprovalGate.tsx` | Real approval and rejection controls |
| `components/EventLog.tsx` | Animated audit event timeline |
| `components/Metrics.tsx` | Reliability metrics view |
| `components/URLShortener.tsx` | Real URL shortener demonstration |

---

## 4. Workflow Lifecycle

The workflow follows this general path:

```text
Requirement Intake
        |
        v
Requirement Assessment
        |
        +--> Ambiguous? ---- yes ---> SAFE_STOP / Clarification
        |                                  |
        |                                  v
        |                             Re-planning
        v
Architecture + Risk Analysis
        |
        v
Task Planning and Dependencies
        |
        v
Implementation Manifest
        |
        +-------------------+
        |                   |
        v                   v
     Tests              Security
        |                   |
        +---------+---------+
                  v
          Validation Gate
                  |
        +---------+---------+
        |                   |
        v                   v
 Approval Required?       Release Gate
        |                   |
        v                   v
Human Approval       RELEASE_READY / SAFE_STOP
```

### LangGraph stages

The compiled graph in `orchestrator/graph.py` contains these nodes:

1. `requirements`
2. `architecture`
3. `planning`
4. `implementation`
5. `validation`

The requirements node conditionally routes ambiguous work to an end state. Non-ambiguous work proceeds through the remaining graph nodes. Architecture and Risk are represented as synchronized analysis outputs in the shared state and frontend graph.

### State preservation

`WorkflowState` preserves:

- Workflow ID.
- Workflow status.
- Current stage.
- Current agent.
- Original requirement.
- Requirement version.
- Normalized requirement.
- Requirement type.
- Structured assessment.
- Acceptance criteria.
- Ambiguities.
- Assumptions.
- Risk level.
- Architecture analysis.
- Tasks and dependencies.
- Changed-file manifest.
- Test results.
- Security results.
- Retry count.
- Rollback count.
- Approval state and approver identity.
- Decision lineage.
- Audit events.
- Start and completion timestamps.

---

## 5. Requirement Assessment

The requirement agent creates a `RequirementAssessment` containing:

- `normalized_requirement`
- `requirement_type`
- `acceptance_criteria`
- `ambiguities`
- `assumptions`
- `risk_level`
- `confidence`
- `security_considerations`
- `non_functional_requirements`
- `impacted_components`
- `recommended_next_step`
- `source`

The `source` value identifies whether the result came from `openai` or the deterministic fallback.

### Deterministic fallback

The fallback deliberately classifies requirements conservatively:

- Greenfield requirements receive low risk unless uncertainty is present.
- Brownfield changes receive medium risk and require approval.
- Destructive terms such as delete, remove, drop, destroy, or purge receive high risk.
- Vague performance terms such as popular, faster, better, or optimize create ambiguity.
- Ambiguity produces a safe-stop instead of silently inventing requirements.

### Optional OpenAI path

OpenAI is enabled only when both variables are configured:

```env
OPENAI_API_KEY=your-key
USE_LLM=true
OPENAI_MODEL=gpt-4o-mini
```

The service uses a timeout and bounded client retry. Invalid or unavailable model output does not bypass the deterministic fallback or policy gates.

---

## 6. Risk and Governance

### Risk levels

- **LOW:** Autonomous analysis, planning, implementation manifest, and validation may proceed.
- **MEDIUM:** Workflow pauses for human approval before release.
- **HIGH:** Workflow pauses for explicit human approval; destructive operations are never released automatically.
- **AMBIGUOUS:** Workflow enters safe-stop until missing information is clarified.

### Approval states

- `NOT_REQUIRED`
- `PENDING`
- `APPROVED`
- `REJECTED`

### Release gate

A workflow can become `RELEASE_READY` only when:

- A normalized requirement exists.
- Test evidence reports pass.
- Security evidence reports pass.
- Required approval is approved or not required.
- No policy condition blocks release.

The React application never decides risk, approval requirement, test result, security result, or release readiness. It only renders backend state and submits permitted actions.

---

## 7. URL Shortener Product

### API endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Backend health check |
| `POST` | `/api/v1/urls` | Create a short URL |
| `GET` | `/api/v1/urls/{short_code}` | Read URL information |
| `GET` | `/api/v1/urls/{short_code}/analytics` | Read click count |
| `DELETE` | `/api/v1/urls/{short_code}` | Disable a URL |
| `GET` | `/{short_code}` | Redirect to the original URL |

### URL behavior

- Only HTTP and HTTPS URLs are accepted through `AnyHttpUrl`.
- Short codes use six random alphanumeric characters.
- Up to five collision attempts are made.
- Expired links return HTTP 410.
- Unknown or disabled links return HTTP 404.
- Successful redirects increment click count.
- Optional expiration must be in the future.
- Existing URLs without an expiration continue to work.

### Data model

`URLRecord` stores:

- ID.
- Short code.
- Original URL.
- Creation time.
- Optional expiration time.
- Active flag.
- Aggregate click count.

---

## 8. Workflow API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/api/v1/workflows` | Start a workflow |
| `GET` | `/api/v1/workflows` | List workflow history |
| `GET` | `/api/v1/workflows/{workflow_id}` | Read workflow detail |
| `GET` | `/api/v1/workflows/{workflow_id}/events` | Read audit events |
| `POST` | `/api/v1/workflows/{workflow_id}/approve` | Approve a pending workflow |
| `POST` | `/api/v1/workflows/{workflow_id}/reject` | Reject a pending workflow |
| `POST` | `/api/v1/workflows/{workflow_id}/clarify` | Add clarification and re-plan |
| `POST` | `/api/v1/workflows/{workflow_id}/rollback` | Restore checkpoint and safe-stop |
| `GET` | `/api/v1/metrics` | Read workflow metrics |

---

## 9. Frontend Demonstration

### Dashboard

The Dashboard renders:

- Total workflows.
- Release-ready count.
- Approval queue.
- Safe stops.
- Latest workflow.
- Workflow graph.
- Risk and current status.
- Requirement analysis.
- Task decomposition.
- Audit events.

### New Run

The New Run page sends the actual textarea value to `POST /api/v1/workflows`. Scenario cards are only shortcuts that populate the input; the backend analyzes the submitted text.

Available scenarios:

1. Greenfield URL API.
2. Brownfield expiration support.
3. Ambiguous performance requirement.
4. High-risk deletion operation.
5. Requirement change involving administrator recovery.

### Workflows

The Workflows page loads real history from the backend. Selecting a workflow displays its detail state, including:

- Workflow ID.
- Status.
- Requirement type.
- Requirement version.
- Risk.
- Current stage.
- Current agent.
- Retry count.
- Approval status.
- Duration.
- Graph.
- Requirement assessment.
- Validation gates.
- Task dependencies.
- Audit trail.

### URL Demo

The URL Demo calls the real FastAPI URL endpoint. It does not use mock short links. The API health indicator comes from `/health`, and creation is disabled when the backend is offline.

### Polling

The frontend polls active workflow state approximately every 1.5 seconds. Polling stops for terminal or waiting states. There are no frontend timers that invent workflow progress.

---

## 10. Auditability and Decision Lineage

Each workflow event records:

- Timestamp.
- Stage.
- Agent or tool.
- Action.
- Status.
- Attempt.
- Optional detail.

Examples include:

- Requirement normalization.
- LLM structured assessment.
- LLM fallback.
- Architecture analysis.
- Planning.
- Implementation manifest creation.
- Test execution.
- Security validation.
- Safe-stop.
- Approval request.
- Approval or rejection.
- Clarification received.
- Release evaluation.
- Rollback.

Architecture decisions include a decision, reason, trade-off, and mitigation context where applicable.

---

## 11. Rollback

A checkpoint is captured before workflow execution. The rollback endpoint:

1. Finds the workflow checkpoint.
2. Restores the pre-execution workflow state.
3. Preserves the workflow ID.
4. Increments `rollback_count`.
5. Changes status to `SAFE_STOP`.
6. Changes current agent to the Policy Engine.
7. Records a rollback event.
8. Requires human review before any further action.

This is workflow-state rollback. It is not repository-code rollback because the current implementation agent records a changed-file manifest instead of applying generated patches.

---

## 12. Metrics

The metrics endpoint currently reports:

- Total workflows.
- Successful workflows.
- Running workflows.
- Approval queue size.
- Safe-stop count.
- Retry count.
- Rollback count.
- Human intervention count.
- Average duration in seconds.

The frontend displays these values as dashboard cards and a dedicated metrics view.

---

## 13. Scenarios

### Greenfield

**Input:**

```text
Build a URL shortening API that accepts a long URL and returns a unique short URL.
```

**Expected path:**

```text
Assessment -> Architecture -> Planning -> Implementation -> Validation -> Release Ready
```

### Brownfield

**Input:**

```text
Add expiration support to existing shortened URLs.
```

**Expected behavior:**

- Classified as brownfield.
- Medium risk.
- Impact analysis is recorded.
- Existing URLs remain compatible.
- Workflow waits for approval.
- Approval can move it to release ready.

### Ambiguous

**Input:**

```text
Make popular URLs faster.
```

**Expected behavior:**

- Classified as ambiguous.
- Missing popularity, scale, latency, and cache constraints are recorded.
- Workflow safe-stops.
- User can submit clarification.
- Requirement version increments.
- Workflow re-enters assessment and planning.

### High risk

**Input:**

```text
Permanently delete all expired URLs.
```

**Expected behavior:**

- Classified as high risk.
- Human approval is required.
- Automatic release is blocked until approval.

### Requirement change

**Version 1:**

```text
URLs should expire after a specified date.
```

**Version 2:**

```text
Expired URLs must remain recoverable by administrators for 30 days.
```

The current clarification endpoint increments the requirement version and re-runs assessment. Full task-level invalidation and preservation of unaffected work is identified as a production enhancement.

---

## 14. Setup

### Backend

From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URLs:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

The frontend reads:

```env
VITE_API_BASE_URL=http://localhost:8000
```

The example is in `frontend/.env.example`.

### Docker

```powershell
docker build -t agentic-url-shortener .
docker run -p 8000:8000 agentic-url-shortener
```

---

## 15. Quality and Security

### Backend tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The current suite covers:

- URL creation.
- Redirects.
- Analytics.
- Unsafe URL rejection.
- Expiration validation.
- Ambiguity detection.
- Assessment detail.
- Greenfield workflow.
- Brownfield approval.
- High-risk approval.
- Health endpoint.
- Workflow history.
- Clarification and version increment.
- Rollback checkpoint restoration.

### Static checks

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m bandit -r app orchestrator -q
.\.venv\Scripts\python.exe -m pip_audit
```

### Frontend check

```powershell
cd frontend
npm run build
```

### Security controls

- Secrets are loaded from environment variables.
- `.env` is ignored by Git.
- OpenAI keys are not hardcoded or logged.
- URLs are validated at the API boundary.
- Destructive requirements require approval.
- Ambiguous requirements safe-stop.
- Test and security evidence comes from backend tools, not frontend claims.
- CORS is restricted to local Vite development origins.

---

## 16. Current Verification Result

At the time of this document:

- Backend tests: `10 passed`.
- Ruff: passed.
- Bandit: passed with reviewed low-risk subprocess suppressions.
- pip-audit: no known vulnerabilities after dependency updates.
- Frontend TypeScript/Vite build: passed.
- Editor diagnostics: no errors.
- Live backend health check: passed.
- Live frontend HTTP check: passed.
- CORS preflight for `http://localhost:5173`: passed.

FastAPI, Starlette, and LangGraph may emit dependency deprecation warnings under Python 3.14. These warnings do not currently fail the test suite.

---

## 17. Limitations and Honest Assessment

The project is a strong controlled-autonomy prototype, but it is not a production distributed platform.

Current limitations:

1. Workflow state is in process memory and is lost when the backend restarts.
2. Workflow execution is synchronous; polling observes state but does not show long-running worker transitions.
3. Architecture and Risk are represented as synchronized state outputs, but they are not independent concurrently running worker processes.
4. Retry state exists, but a complete diagnosis, corrective patch, and retry loop is not implemented.
5. Rollback restores workflow state, not repository source files.
6. The implementation agent records a changed-file manifest instead of applying generated code patches.
7. Security validation is a deterministic policy result in the prototype; CI remains the place for full scanner execution.
8. Metrics do not yet include full MTTR, failure rate, token cost, or production latency telemetry.
9. Analytics stores aggregate click count rather than individual redirect event rows with timestamp, referrer, and user-agent data.
10. Requirement change re-planning increments version and reruns assessment, but does not yet perform complete task invalidation mapping.
11. Authentication, RBAC, rate limiting, migrations, distributed workers, and enterprise observability are out of scope.

These limitations are explicitly documented because defensible engineering judgment includes identifying what the prototype does not yet prove.

---

## 18. Recommended Production Evolution

If this prototype were advanced beyond the interview assignment, the next steps would be:

1. Persist workflow state and checkpoints in a database.
2. Run LangGraph stages through a worker queue.
3. Add true parallel branch execution and synchronization barriers.
4. Add diagnosis and corrective-action nodes.
5. Add Git commit/checkpoint integration for repository rollback.
6. Execute Ruff, Bandit, and pip-audit as workflow evidence with parsed results.
7. Add task invalidation and requirement-diff impact analysis.
8. Persist redirect events for richer analytics.
9. Add authentication and role-based approval permissions.
10. Add OpenTelemetry, metrics export, and durable audit storage.
11. Add CI with pytest, Ruff, Bandit, and pip-audit.
12. Add rate limiting and production database migrations.

---

## 19. Interview Walkthrough

A concise demonstration can follow this sequence:

1. Start the backend and frontend.
2. Show the real `API ONLINE` indicator.
3. Open New Run and select Brownfield.
4. Start the workflow.
5. Open Workflow Detail.
6. Explain requirement type, risk, current agent, tasks, graph, gates, and events.
7. Approve the workflow through the frontend.
8. Show the release-ready result.
9. Start the ambiguous scenario.
10. Show the safe-stop and ambiguity questions.
11. Submit measurable clarification.
12. Show requirement version 2 and re-planning.
13. Start the high-risk destructive scenario.
14. Show the approval checkpoint.
15. Demonstrate rollback through the API if needed.
16. Open URL Demo.
17. Create a real short URL, redirect it, and inspect analytics.
18. Open Metrics to show workflow reliability signals.
19. Finish by showing the test, security, and dependency audit commands.

The strongest message is not that the system lets AI make unrestricted changes. The strongest message is that it makes AI-assisted engineering observable, testable, reviewable, and governable.
