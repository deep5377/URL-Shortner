from orchestrator.state import WorkflowState

MAX_RETRIES = 3


def classify_risk(requirement_type: str, ambiguities: list[str]) -> str:
	if ambiguities:
		return "HIGH"
	return {"GREENFIELD": "LOW", "BROWNFIELD": "MEDIUM"}.get(requirement_type, "MEDIUM")


def approval_required(state: WorkflowState) -> bool:
	return state.risk_level in {"MEDIUM", "HIGH"}


def can_release(state: WorkflowState) -> bool:
	return (
		state.test_results.get("passed") is True
		and state.security_results.get("passed") is True
		and bool(state.normalized_requirement)
		and (not approval_required(state) or state.approval_status == "APPROVED")
	)
