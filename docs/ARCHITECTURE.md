# Architecture Overview

## Runtime

FastAPI exposes the URL service and workflow control plane. SQLAlchemy persists URL records in SQLite. The React/Vite control center calls the API through one typed client and renders backend state.

## Workflow

`orchestrator/graph.py` compiles a LangGraph state graph with conditional routing:

```text
requirements -> architecture/risk -> planning -> implementation -> validation
       |                                               |
       +-> SAFE_STOP                                  +-> approval/release gate
```

`WorkflowState` is the cross-stage context. It preserves the original requirement, structured assessment, tasks and dependencies, node statuses, decisions, changed-file manifest, validation evidence, approval identity, retry/rollback counters, and audit events.

The Architecture and Risk branches are represented as synchronized independent outputs. Policy determines risk and approval; deterministic tools provide pytest and security evidence; React never decides release readiness.

## Governance

- Ambiguity routes to `SAFE_STOP` until clarification is submitted.
- Medium/high-risk work pauses at `AWAITING_APPROVAL`.
- Release requires test evidence, security evidence, normalized requirements, and approval when policy requires it.
- Rollback restores the captured pre-execution workflow checkpoint, records an event, and safe-stops for review.
- OpenAI structured assessment is opt-in via `OPENAI_API_KEY` and `USE_LLM=true`; invalid or unavailable model output falls back to deterministic assessment and records an audit event.

## Prototype boundaries

Workflow state is currently in process memory and execution is synchronous. The implementation agent records a reviewable change manifest rather than applying generated repository patches. Production evolution should add durable workflow checkpoints, worker execution, real scanner adapters, diagnosis/rollback transactions, and requirement-version impact analysis.