# Test Plan

## Automated coverage

- URL API: valid creation, redirect, click analytics, unsafe schemes, expiration, and unknown codes.
- Agents: requirement normalization, classification, ambiguity detection, and risk assignment.
- Requirement assessment: confidence, acceptance criteria, impact, security considerations, and deterministic fallback when the LLM is unavailable.
- Workflow: greenfield release, brownfield approval gate, and ambiguous safe-stop.

Run `python -m pytest -q` from the project virtual environment.

## Release checks

Run `ruff check .` and `bandit -r app orchestrator -q`. Validation evidence is recorded in workflow state and events. A scanner failure is not treated as a pass.

## Known prototype limits

Analytics stores an aggregate click count rather than raw event rows. Workflow state is in memory, and implementation is represented as an auditable change manifest rather than applying generated patches. Production deployment should add durable workflow persistence, authentication, rate limiting, migrations, and distributed observability.
