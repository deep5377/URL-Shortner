Absolutely. Since `PRD.md` is going to be the **main source-of-truth document** and we're intentionally not creating separate HLD/LLD/ADR files, I would make this PRD detailed enough to cover requirements, architecture, orchestration, APIs, data, governance, scenarios, risks, and acceptance criteria.

Copy the following directly into `docs\PRD.md`.

# Product Requirements Document (PRD)

## Agentic Software Engineering System — URL Shortener

**Version:** 1.0
**Status:** Prototype / Interview Assignment
**Target Delivery:** 2–3 Days
**Primary Language:** Python 3.12
**Application:** URL Shortener
**Agentic Orchestration:** LangGraph
**LLM Provider:** OpenAI
**Database:** SQLite

---

# 1. Executive Summary

This project implements a working Agentic Software Engineering System that transforms natural-language software requirements into reviewable engineering outcomes through a controlled, stateful, and auditable execution workflow.

A URL shortener service is used as the engineering workload for demonstrating the system. The URL shortener supports core URL creation and redirection capabilities, analytics, expiration, validation, and reliability behavior.

The primary objective of the project is not only to generate application code. The system must demonstrate an end-to-end Software Development Life Cycle (SDLC) workflow covering:

* Requirement understanding
* Ambiguity detection
* Requirement normalization
* Architecture reasoning
* Task decomposition
* Dependency management
* Implementation
* Testing
* Security validation
* Documentation
* Release readiness
* Human approval
* Retry and recovery
* Dynamic re-planning
* Auditability
* Controlled agent autonomy

Agents may perform engineering work autonomously within explicitly defined boundaries. Deterministic tools validate generated work, while humans retain authority over high-impact actions and final release decisions.

---

# 2. Problem Statement

Traditional AI coding assistants primarily respond to individual prompts and generate isolated code changes.

Real software engineering requires significantly more than code generation.

A requirement must be:

1. Understood
2. Normalized
3. Evaluated for ambiguity
4. Converted into acceptance criteria
5. Decomposed into engineering tasks
6. Mapped to dependencies
7. Evaluated for architectural impact
8. Implemented
9. Tested
10. Security reviewed
11. Validated
12. Documented
13. Approved
14. Prepared for release

Failures can occur at any stage.

Requirements may also change after downstream engineering work has already begun.

The system therefore needs a stateful orchestration model capable of reasoning about dependencies, maintaining context, validating outputs, retrying recoverable failures, stopping unsafe execution, and involving humans when required.

---

# 3. Product Vision

Build a lightweight but production-oriented prototype demonstrating how AI agents can participate in software engineering while operating under explicit governance, validation, and human oversight.

The core principle is:

> Agents execute within defined autonomy boundaries; deterministic systems validate execution; humans retain oversight and final authority.

The system should demonstrate meaningful agentic behavior without unnecessary infrastructure complexity.

---

# 4. Goals

The system shall demonstrate:

* End-to-end requirement-to-engineering-output automation
* Stateful multi-step agent execution
* Explicit task dependency graphs
* Sequential and parallel execution
* Synchronization of parallel work
* Entry and exit validation gates
* Cross-stage context preservation
* Decision lineage
* Human approval checkpoints
* Bounded retries
* Failure diagnosis
* Fallback behavior
* Safe-stop behavior
* Rollback capability
* Dynamic re-planning
* Security guardrails
* Change-control policies
* Audit logging
* Reliability metrics
* Production-quality URL shortener functionality
* Unit and integration testing
* Reproducible local execution

---

# 5. Non-Goals

The prototype will intentionally avoid unnecessary production infrastructure.

The following are out of scope:

* Kubernetes
* Kafka
* Distributed agent workers
* Service mesh
* Vector databases
* RAG infrastructure
* Model fine-tuning
* Multiple LLM providers
* Multiple specialized LLM models
* Production cloud deployment
* Full authentication platform
* Enterprise secrets management
* Full observability platforms such as Datadog or Grafana
* Production-grade distributed rollback
* Large-scale load testing

These capabilities may be described as future production improvements where appropriate.

---

# 6. Technology Stack

The system will use:

| Area                      | Technology               |
| ------------------------- | ------------------------ |
| Programming Language      | Python 3.12              |
| REST API                  | FastAPI                  |
| Agent Orchestration       | LangGraph                |
| LLM                       | Lightweight OpenAI model |
| LLM Integration           | OpenAI Python SDK        |
| Validation                | Pydantic                 |
| ORM                       | SQLAlchemy               |
| Database                  | SQLite                   |
| Unit Testing              | pytest                   |
| API / Integration Testing | HTTPX                    |
| Linting                   | Ruff                     |
| Static Security Analysis  | Bandit                   |
| Dependency Security       | pip-audit                |
| Source Control            | Git                      |
| Containerization          | Docker                   |
| CI                        | GitHub Actions           |

The architecture intentionally uses a single lightweight LLM.

Agent specialization will be achieved through:

* Role-specific instructions
* Structured input
* Structured output
* Shared workflow context
* Available tools
* Permissions
* Policies
* Autonomy boundaries

Different models are not required for each agent.

---

# 7. High-Level Architecture

The solution contains two primary functional areas:

## 7.1 URL Shortener Application

Responsible for:

* URL creation
* Short-code generation
* URL redirection
* Expiration
* Analytics
* Persistence
* Input validation

High-level flow:

```text
Client
  |
  v
FastAPI
  |
  v
URL Service
  |
  v
SQLAlchemy
  |
  v
SQLite
```

## 7.2 Agentic SDLC Orchestrator

Responsible for transforming engineering requirements into validated engineering outcomes.

```text
Requirement
    |
    v
Requirement Analysis
    |
    v
Architecture / Risk Analysis
    |
    v
Task Planning
    |
    v
Implementation
    |
    +----------------+
    |                |
    v                v
Testing          Security Checks
    |                |
    +-------+--------+
            |
            v
       Validation Gate
          /      \
       PASS      FAIL
        |          |
        v          v
    Approval    Diagnose
        |          |
        |       Retry/Re-plan
        v
 Documentation
        |
        v
Release Readiness
```

The workflow is not a simple fixed sequential chain.

The orchestrator must support:

* Conditional routing
* Parallel execution
* Synchronization
* Backward transitions
* Retries
* Approval pauses
* Safe stops
* Re-planning

---

# 8. Core Architectural Principle

The system separates reasoning, orchestration, execution, validation, and governance.

## LLM

Responsible for:

* Understanding requirements
* Identifying ambiguity
* Generating acceptance criteria
* Architecture reasoning
* Planning
* Implementation proposals
* Failure diagnosis
* Security reasoning
* Documentation generation

## LangGraph

Responsible for:

* Workflow orchestration
* State management
* Routing
* Branching
* Synchronization
* Retry routing
* Human-in-the-loop pauses
* Re-planning

## Deterministic Tools

Responsible for:

* Running pytest
* Running Ruff
* Running Bandit
* Running pip-audit
* File operations
* Git operations
* Validation
* Metrics calculation

## Policy Layer

Responsible for:

* Risk rules
* Approval requirements
* Retry limits
* Release gates
* Safe-stop rules

## Human

Responsible for:

* High-impact approvals
* Resolving critical ambiguity
* Reviewing high-risk changes
* Final quality ownership

---

# 9. URL Shortener Functional Requirements

## URL-001 — Create Short URL

The system shall accept a valid long URL and generate a unique short code.

Example request:

```json
{
  "url": "https://example.com/products/engineering"
}
```

Example response:

```json
{
  "short_code": "Ab12Cd",
  "short_url": "http://localhost:8000/Ab12Cd",
  "original_url": "https://example.com/products/engineering"
}
```

### Acceptance Criteria

* URL is validated.
* Unique short code is generated.
* Mapping is persisted.
* Response contains short code and short URL.
* Invalid URLs are rejected.

---

## URL-002 — Redirect Short URL

The system shall redirect a valid short code to its original URL.

### Acceptance Criteria

* Existing active code redirects successfully.
* Unknown code returns 404.
* Expired code returns appropriate error.
* Redirect event is recorded for analytics.

---

## URL-003 — URL Expiration

The system shall optionally support expiration timestamps.

### Acceptance Criteria

* URL may be created without expiration.
* URL may contain an expiration timestamp.
* Expired URLs cannot redirect normally.
* Existing URLs without expiration continue functioning.

---

## URL-004 — Analytics

The system shall record basic redirect analytics.

Minimum information:

* Short code
* Click count
* Timestamp

Optional information:

* Referrer
* User agent

Raw sensitive client information should not be persisted unless required.

---

## URL-005 — Short-Code Collision Handling

Short-code generation must handle collisions.

### Rules

* Generate short code.
* Check uniqueness.
* Retry on collision.
* Maximum collision retries shall be bounded.
* Persistent collision failure returns controlled application error.

---

# 10. Requirement Understanding

## AG-001 — Requirement Intake

The system shall accept natural-language software requirements.

Example:

```text
Add expiration support to short URLs.
```

The original requirement must always be preserved.

---

## AG-002 — Requirement Normalization

The Requirement Agent shall transform raw requirements into structured engineering requirements.

Output must include:

* Original requirement
* Normalized requirement
* Requirement type
* Acceptance criteria
* Ambiguities
* Assumptions
* Risk classification

---

## AG-003 — Requirement Classification

Requirements shall be classified as:

* Greenfield
* Brownfield
* Ambiguous

Additional risk classification may also be assigned.

---

## AG-004 — Ambiguity Detection

The system shall identify requirements that cannot safely be implemented without additional interpretation.

Example:

```text
Make popular URLs faster.
```

Potential ambiguities include:

* Definition of popular
* Expected traffic
* Required latency
* Measurement percentile
* Cache freshness
* Infrastructure constraints

The system shall not silently treat uncertain assumptions as confirmed facts.

---

# 11. Task Decomposition

## PLAN-001 — Engineering Task Generation

The Planning Agent shall convert normalized requirements into actionable engineering tasks.

Each task shall contain:

* Task ID
* Description
* Dependencies
* Status
* Risk
* Required validation

Example:

```text
T1 - Update database model
T2 - Update API schema
T3 - Modify URL creation logic
T4 - Modify redirect behavior
T5 - Add unit tests
T6 - Add integration tests
T7 - Update documentation
```

---

## PLAN-002 — Dependency Graph

Tasks shall be represented as an explicit dependency graph.

Example:

```text
T1
|-- T2
|-- T3
|-- T4

T2 + T3 + T4
      |
      v
     T5
      |
      v
     T6
      |
      v
     T7
```

Independent tasks may execute in parallel.

Dependent tasks shall not execute until prerequisites are complete.

---

# 12. Brownfield Codebase Reasoning

## CODE-001 — Impact Analysis

For brownfield requirements, the system shall identify affected areas before modifying code.

Potential impacted areas:

* API
* Pydantic schemas
* SQLAlchemy models
* Services
* Database
* Tests
* Documentation
* Security controls

Example:

```text
Requirement:
Add expiration support.

Potential impact:

models.py
schemas.py
url_service.py
routes.py
test_urls.py
```

---

## CODE-002 — Backward Compatibility

The system shall identify potential compatibility risks.

For example:

Existing URLs created before expiration support must continue functioning.

---

# 13. Agent Roles

The prototype will use logical specialized agents backed by the same LLM service.

## 13.1 Requirement Agent

Responsibilities:

* Understand intent
* Normalize requirement
* Identify ambiguity
* Generate acceptance criteria
* Identify assumptions
* Classify requirement
* Initial risk assessment

## 13.2 Architecture Agent

Responsibilities:

* Analyze system impact
* Identify affected components
* Identify data/API changes
* Identify compatibility risks
* Recommend technical approach

## 13.3 Planning Agent

Responsibilities:

* Generate tasks
* Identify dependencies
* Create execution sequence
* Identify parallelizable tasks
* Define validation requirements

## 13.4 Implementation Agent

Responsibilities:

* Generate or modify code
* Follow approved plan
* Make bounded changes
* Preserve existing behavior unless explicitly changed

## 13.5 Test / Diagnosis Agent

Responsibilities:

* Analyze required tests
* Interpret test failures
* Identify likely root causes
* Recommend minimal corrective action

Actual tests are executed by deterministic tools.

## 13.6 Security Agent

Responsibilities:

* Review security implications
* Interpret static analysis findings
* Identify unsafe changes
* Recommend mitigation

## 13.7 Documentation / Release Agent

Responsibilities:

* Summarize changes
* Generate engineering documentation
* Evaluate release readiness
* Document limitations
* Produce final engineering summary

---

# 14. Shared Workflow State

The workflow must preserve context between agents.

Conceptual state:

```text
workflow_id
status
current_stage

raw_requirement
normalized_requirement
requirement_type
requirement_version

acceptance_criteria
ambiguities
assumptions

risk_level

architecture_analysis

tasks
task_dependencies

changed_files

test_results
security_results

retry_count
rollback_count

approval_status

decisions
events

started_at
completed_at
```

Agents shall not depend solely on conversational memory.

Important workflow information must be represented explicitly in state.

---

# 15. Workflow Orchestration

## ORCH-001 — Stateful Execution

The workflow shall preserve state across execution stages.

---

## ORCH-002 — Sequential Execution

Dependent stages shall execute sequentially where required.

Example:

```text
Requirement Analysis
        |
        v
Planning
        |
        v
Implementation
```

---

## ORCH-003 — Parallel Execution

Independent activities should be capable of executing in parallel.

Example:

```text
              Requirement
                   |
         +---------+---------+
         |                   |
         v                   v
 Architecture Analysis    Risk Analysis
         |                   |
         +---------+---------+
                   |
                   v
                Planning
```

---

## ORCH-004 — Synchronization

Downstream nodes requiring multiple upstream outputs shall wait until required dependencies complete.

---

## ORCH-005 — Conditional Routing

Workflow routing shall depend on state.

Examples:

```text
Tests PASS -> Security/Release Validation

Tests FAIL -> Diagnosis

High Risk -> Human Approval

Critical Risk -> SAFE_STOP
```

---

# 16. Entry and Exit Gates

Each major stage shall have explicit validation conditions.

## Requirement Gate

Required:

* Normalized requirement exists
* Acceptance criteria exist
* Risk level assigned
* Ambiguities evaluated

## Implementation Gate

Required:

* Requirement accepted
* Plan exists
* Dependencies identified
* No unresolved blocking ambiguity
* Required approvals obtained

## Validation Gate

Required:

* Tests executed
* Lint executed
* Security checks executed

## Release Gate

Required:

* Required tests pass
* No blocking security findings
* Documentation generated
* Required approval exists
* Rollback information exists
* No unresolved critical risks

---

# 17. Controlled Autonomy

Agent autonomy shall depend on risk.

## LOW Risk

Agents may:

* Plan
* Implement
* Test
* Validate

Release may proceed according to configured policy.

## MEDIUM Risk

Agents may:

* Analyze
* Plan
* Implement
* Test

Human approval required before final release readiness.

## HIGH Risk

Human approval required before high-impact implementation.

## CRITICAL Risk

Automatic execution prohibited.

Workflow enters:

```text
SAFE_STOP
```

---

# 18. Human-in-the-Loop

The workflow shall support explicit human approval.

Possible states:

```text
NOT_REQUIRED
PENDING
APPROVED
REJECTED
```

Example API behavior:

```text
POST /api/v1/workflows/{id}/approve

POST /api/v1/workflows/{id}/reject
```

The workflow shall preserve approval identity/status and decision timestamp where available.

---

# 19. Retry Strategy

## REL-001 — Bounded Retry

Automatic retries must always be bounded.

Default:

```text
MAX_RETRIES = 3
```

Example:

```text
Test Failure
     |
     v
Diagnosis
     |
     v
Retry Count < 3?
   /       \
 YES       NO
  |         |
  v         v
Fix      SAFE_STOP
  |
  v
Re-test
```

Every retry shall be recorded.

---

# 20. Failure Classification

Failures should be classified where practical.

Potential classes:

* Recoverable implementation failure
* Test failure
* Tool failure
* LLM failure
* Security violation
* Policy violation
* Invalid structured output
* Unresolved ambiguity
* Retry exhaustion

Failure classification determines routing behavior.

---

# 21. Fallback

The system shall provide controlled fallback behavior.

Examples:

* Invalid LLM structured output -> retry once with stricter instruction
* LLM unavailable -> workflow pauses safely
* Tool unavailable -> workflow records failure
* Test infrastructure failure -> do not treat as test success
* Security scanner failure -> do not automatically mark security validation passed

The system must fail closed for high-impact validation decisions.

---

# 22. Safe Stop

## GOV-001 — Safe Stop

The workflow shall enter `SAFE_STOP` when automatic continuation would be unsafe.

Examples:

* Critical security finding
* Retry exhaustion
* Destructive operation without approval
* Invalid workflow state
* Required validation unavailable
* Unresolved high-impact ambiguity

Safe stop must preserve:

* Current state
* Failure reason
* Previous decisions
* Test/security results
* Retry history

---

# 23. Rollback

The prototype shall demonstrate rollback at an appropriate level.

Possible rollback information:

* Git commit/checkpoint
* Changed files
* Previous workflow state
* Previous known-good status

Rollback operations shall be bounded and auditable.

The prototype does not require enterprise distributed transaction rollback.

---

# 24. Dynamic Re-Planning

## ORCH-006 — Requirement Change Detection

The system shall support requirement versioning.

Example:

### Version 1

```text
URLs should expire after a specified date.
```

### Version 2

```text
Expired URLs must remain recoverable by administrators for 30 days.
```

The system shall identify that upstream assumptions changed.

---

## ORCH-007 — Impact-Based Re-Planning

When requirements change, the system should determine affected tasks.

Example:

```text
Database model        INVALIDATED
Expiration logic      INVALIDATED
Admin recovery API    NEW
Existing creation API UNAFFECTED
```

Only affected downstream work should be re-planned where practical.

All re-planning decisions must be recorded.

---

# 25. LLM Service

All agents shall access the OpenAI API through a centralized LLM service.

Conceptual architecture:

```text
Agents
  |
  v
LLM Service
  |
  +-- Model configuration
  +-- Timeout handling
  +-- Retry handling
  +-- Structured output
  +-- Logging
  +-- Error handling
  |
  v
OpenAI API
```

Agents should not independently configure OpenAI clients.

---

# 26. Structured Agent Output

Critical agent outputs shall use Pydantic schemas.

Example:

```python
class RequirementAnalysis(BaseModel):
    normalized_requirement: str
    requirement_type: str
    acceptance_criteria: list[str]
    ambiguities: list[str]
    assumptions: list[str]
    risk_level: str
```

Structured outputs improve:

* Reliability
* Validation
* Routing
* Testing
* Auditability

---

# 27. Deterministic Tools

LLMs shall not claim deterministic actions occurred without tool evidence.

The system shall use real tools for:

## Testing

```text
pytest
```

## Linting

```text
ruff check .
```

## Static Security Analysis

```text
bandit
```

## Dependency Vulnerability Analysis

```text
pip-audit
```

## Version Control

```text
Git
```

LLMs may interpret tool output but must not fabricate execution results.

---

# 28. Security Requirements

## SEC-001 — Secret Protection

The OpenAI API key shall:

* Be loaded from environment variables
* Never be hardcoded
* Never be committed to Git
* Never be included in logs

`.env` shall be excluded through `.gitignore`.

---

## SEC-002 — Input Validation

All API input shall be validated using Pydantic.

---

## SEC-003 — URL Validation

Unsafe or invalid URL input shall be rejected.

Supported protocols should initially be limited to:

```text
http
https
```

Protocols such as the following should not be accepted:

```text
javascript:
file:
```

---

## SEC-004 — Generated Code Validation

Generated or modified code shall not automatically be considered safe.

It must pass applicable:

* Tests
* Ruff
* Bandit
* pip-audit
* Policy checks

before release readiness.

---

## SEC-005 — Destructive Action Protection

Destructive or high-impact actions shall require human approval.

---

# 29. Change Control

Every implementation change should be associated with:

* Workflow ID
* Requirement version
* Task ID where applicable
* Changed files
* Validation result
* Approval state

Git shall provide source-control history.

---

# 30. Auditability

The system shall maintain workflow event history.

Example event:

```json
{
  "workflow_id": "WF-001",
  "agent": "test_agent",
  "action": "run_tests",
  "status": "FAILED",
  "attempt": 1,
  "duration_ms": 1800
}
```

Events should capture where practical:

* Workflow ID
* Timestamp
* Stage
* Agent/tool
* Action
* Status
* Attempt
* Duration
* Failure reason
* Requirement version

---

# 31. Decision Lineage

Important engineering decisions shall be recorded.

Example:

```json
{
  "decision": "Use SQLite for prototype persistence",
  "reason": "Simple reproducible local setup",
  "alternative": "PostgreSQL",
  "tradeoff": "Limited production scalability"
}
```

Decision lineage allows reviewers to understand why the system selected a particular approach.

---

# 32. Reliability Metrics

The orchestration layer shall track where practical:

## Workflow Success Rate

Percentage of workflows successfully reaching release-ready status.

## Retry Frequency

Number or percentage of workflows requiring retries.

## Rollback Frequency

Number of rollback events.

## Safe-Stop Frequency

Number of workflows entering safe-stop.

## Human Intervention Rate

Percentage of workflows requiring approval or intervention.

## End-to-End Latency

Time from workflow start to completion.

## MTTR

Approximate mean time to recover from recoverable workflow failures.

---

# 33. URL Shortener Data Model

## URL Record

Suggested fields:

```text
id
short_code
original_url
created_at
expires_at
is_active
click_count
```

## Workflow Record

Suggested fields:

```text
workflow_id
requirement
requirement_version
status
current_stage
risk_level
retry_count
approval_status
started_at
completed_at
```

Detailed workflow state may initially be persisted as structured JSON where this simplifies the prototype.

---

# 34. API Requirements

## Application APIs

### Create URL

```text
POST /api/v1/urls
```

### Get URL information

```text
GET /api/v1/urls/{short_code}
```

### Redirect

```text
GET /{short_code}
```

### Analytics

```text
GET /api/v1/urls/{short_code}/analytics
```

### Delete / Disable URL

```text
DELETE /api/v1/urls/{short_code}
```

---

## Workflow APIs

### Start Workflow

```text
POST /api/v1/workflows
```

### Workflow Status

```text
GET /api/v1/workflows/{workflow_id}
```

### Approve Workflow

```text
POST /api/v1/workflows/{workflow_id}/approve
```

### Reject Workflow

```text
POST /api/v1/workflows/{workflow_id}/reject
```

### Workflow Events

```text
GET /api/v1/workflows/{workflow_id}/events
```

---

# 35. Non-Functional Requirements

## NFR-001 — Maintainability

Code shall be modular and separated between:

* API
* Business logic
* Persistence
* Agent orchestration
* LLM access
* Policies
* Tools

---

## NFR-002 — Testability

Core business and workflow behavior shall be testable without requiring manual API calls.

---

## NFR-003 — Reliability

Workflow failures shall not silently result in release-ready status.

---

## NFR-004 — Security

Secrets must remain outside source control.

Generated code must pass security validation before release readiness.

---

## NFR-005 — Observability

Major workflow transitions shall produce structured events.

---

## NFR-006 — Portability

The application shall run locally using Python and should also support Docker execution.

---

# 36. Required Demonstration Scenarios

The system must demonstrate at least three core scenarios.

---

## Scenario 1 — Greenfield

### Requirement

```text
Build a URL shortening API that accepts a long URL
and returns a unique short URL.
```

### Expected Workflow

```text
Requirement
   |
   v
Normalize
   |
   v
Acceptance Criteria
   |
   v
Architecture
   |
   v
Task Decomposition
   |
   v
Implementation
   |
   v
Testing
   |
   v
Security
   |
   v
Documentation
   |
   v
Release Readiness
```

### Validation

* Short URL generated.
* URL persisted.
* Redirect works.
* Tests pass.
* Security checks pass.

---

# 37. Scenario 2 — Brownfield

### Requirement

```text
Add expiration support to existing short URLs.
```

### Expected Behavior

System performs impact analysis before modification.

Potential affected areas:

```text
models.py
schemas.py
routes.py
url_service.py
test_urls.py
```

### Expected Acceptance Criteria

* New URLs may have expiration.
* Existing URLs remain compatible.
* Expired URLs cannot redirect normally.
* Appropriate tests are added.
* Documentation is updated.

---

# 38. Scenario 3 — Ambiguous

### Requirement

```text
Make popular URLs faster.
```

### Expected Ambiguities

* What defines popular?
* What latency target?
* What traffic level?
* Which percentile?
* Is caching allowed?
* What freshness requirement?

The system shall identify these ambiguities before making high-impact architecture changes.

If assumptions are permitted for demonstration purposes, they must be explicitly recorded.

Example:

```text
Popular = >100 redirects/hour
Target = P95 redirect latency <50 ms
```

---

# 39. Additional Scenario — High Risk

### Requirement

```text
Permanently delete all expired URLs.
```

Expected behavior:

```text
Requirement
    |
    v
Risk Classification
    |
    v
HIGH
    |
    v
HUMAN APPROVAL REQUIRED
```

The agent must not automatically execute destructive behavior.

---

# 40. Additional Scenario — Requirement Change

Initial requirement:

```text
URLs should expire after a specified date.
```

Updated requirement:

```text
Expired URLs must remain recoverable by administrators
for 30 days.
```

Expected:

* Requirement version increments.
* Impact analysis runs.
* Affected tasks are invalidated.
* New tasks are generated.
* Unaffected work is preserved where possible.
* Decision is logged.

---

# 41. Test Strategy

Testing shall include:

## Unit Tests

* Short-code generation
* URL validation
* Expiration logic
* Risk classification
* Policy rules

## API Tests

* URL creation
* Redirect
* Invalid URL
* Unknown short code
* Expired URL
* Analytics

## Workflow Tests

* Greenfield execution
* Brownfield impact analysis
* Ambiguity detection
* Parallel branch synchronization
* Test failure retry
* Retry exhaustion
* Human approval
* Safe stop
* Requirement change
* Re-planning

## Security Tests

* Invalid protocols
* Secret exposure prevention
* High-risk operation blocking
* Failed security gate prevents release

---

# 42. CI Quality Gate

GitHub Actions shall execute at minimum:

```text
Ruff
pytest
Bandit
pip-audit
```

Conceptual pipeline:

```text
Push / Pull Request
        |
        v
       Ruff
        |
        v
      pytest
        |
        v
      Bandit
        |
        v
    pip-audit
        |
        v
      PASS/FAIL
```

A failed required validation shall prevent successful CI completion.

---

# 43. Demo Data

The project shall contain lightweight deterministic demo data.

Files:

```text
data/scenarios.json
data/sample_urls.json
```

`scenarios.json` should contain:

* Greenfield scenario
* Brownfield scenario
* Ambiguous scenario
* High-risk scenario
* Requirement-change scenario

No large external dataset is required.

No ML training data is required.

---

# 44. Error Handling

The system shall return controlled errors instead of exposing stack traces or sensitive information.

Important failure cases:

* Invalid URL
* Short code not found
* Short code expired
* Database failure
* LLM unavailable
* Invalid LLM structured output
* Tool execution failure
* Test failure
* Security validation failure
* Retry exhaustion
* Human rejection

---

# 45. Assumptions

The prototype assumes:

1. A valid OpenAI API key is available.
2. Internet connectivity exists for LLM requests.
3. Python 3.12 is installed for non-Docker execution.
4. Git is available.
5. Workflows operate against the local prototype repository.
6. SQLite is sufficient for demonstration.
7. A single lightweight OpenAI model is sufficient.
8. Human approval is represented through API actions rather than a dedicated frontend.
9. Swagger/OpenAPI is sufficient as the prototype interaction interface.

---

# 46. Engineering Trade-offs

## SQLite vs PostgreSQL

**Selected:** SQLite

Reason:

* Zero infrastructure
* Easy interviewer setup
* Sufficient prototype persistence

Trade-off:

Not intended for high-concurrency production workloads.

Production evolution:

```text
SQLite -> PostgreSQL
```

---

## Single LLM vs Multiple Models

**Selected:** Single lightweight OpenAI model.

Benefits:

* Lower complexity
* Easier debugging
* Lower cost
* Consistent behavior

Agent specialization occurs through prompts, schemas, state, tools, and permissions.

---

## No Vector Database

A vector database is intentionally excluded because the prototype does not have a meaningful semantic retrieval requirement.

Structured requirements and workflow state are better represented through normal structured persistence.

---

## No Frontend

FastAPI Swagger will serve as the primary prototype interface.

This allows engineering effort to focus on orchestration rather than UI development.

---

# 47. Risks

## LLM Non-Determinism

Risk:

Agent output may vary.

Mitigation:

* Pydantic schemas
* Structured output
* Validation
* Deterministic gates
* Bounded retries

## Unsafe Generated Code

Mitigation:

* pytest
* Ruff
* Bandit
* pip-audit
* Human approval

## Infinite Agent Loops

Mitigation:

```text
MAX_RETRIES = 3
```

plus safe-stop.

## Requirement Misinterpretation

Mitigation:

* Preserve original requirement
* Explicit ambiguity detection
* Acceptance criteria
* Assumption tracking
* Human approval when needed

## Secret Exposure

Mitigation:

* `.env`
* `.gitignore`
* Never log API keys

---

# 48. Limitations

The initial prototype may have the following limitations:

* SQLite persistence
* Single-process execution
* Single LLM provider
* Limited repository sandboxing
* Simplified rollback
* Local Git integration
* No distributed worker architecture
* No production deployment automation
* Basic metrics rather than full monitoring platform
* Simplified user/approval identity
* Limited load testing

These limitations are intentional to keep the prototype achievable within the 2–3 day delivery window.

---

# 49. Future Improvements

Potential production evolution:

* PostgreSQL
* Redis caching
* Distributed task workers
* Durable workflow persistence
* OpenTelemetry
* Prometheus/Grafana
* Enterprise authentication
* RBAC
* Strong repository sandboxing
* Cloud deployment
* Advanced policy engine
* Cost/token monitoring
* Multi-model routing when justified
* Automated pull-request generation
* Deployment approvals
* Canary releases
* Advanced rollback

---

# 50. Definition of Done

The prototype is considered complete when:

* URL shortener runs end-to-end.
* Long URLs can be shortened.
* Short URLs redirect successfully.
* Analytics are recorded.
* Expiration behavior is implemented or demonstrated through the brownfield workflow.
* Agentic workflow runs through LangGraph.
* Requirements are normalized.
* Ambiguities can be detected.
* Tasks and dependencies are generated.
* Workflow state is preserved.
* Conditional routing works.
* At least one parallel execution path exists.
* Failed validation can trigger retry.
* Retry count is bounded.
* Retry exhaustion produces safe-stop.
* Human approval can pause/resume a workflow.
* Security policies can block unsafe progression.
* Audit events are captured.
* Requirement changes can trigger re-planning.
* Greenfield scenario is demonstrated.
* Brownfield scenario is demonstrated.
* Ambiguous scenario is demonstrated.
* Unit and integration tests run successfully.
* Ruff runs.
* Bandit runs.
* pip-audit runs.
* Docker can run the application.
* GitHub Actions validates the repository.
* README contains setup and demo instructions.

---

# 51. Final Engineering Principle

The prototype will optimize for controlled, observable engineering automation rather than maximum AI autonomy.

The intended operating model is:

```text
LLM
  |
  | reasoning
  v
LangGraph
  |
  | orchestration
  v
Deterministic Tools
  |
  | execution + validation
  v
Policy Gates
  |
  | governance
  v
Human
  |
  | oversight + approval
  v
Reviewable Engineering Outcome
```

Agents are permitted to execute meaningful multi-step engineering work, but they cannot bypass validation, policy controls, risk gates, or required human approval.

The final system must therefore demonstrate not simply that AI can generate software, but that AI-assisted software engineering can operate through a structured, stateful, testable, auditable, and controlled SDLC process.

This PRD is intentionally detailed enough to replace the separate HLD/LLD/ADR documents we removed. The next file I’d create is `TEST_PLAN.md`, but **implementation should follow this PRD rather than adding more design documents**.
