from orchestrator.llm_service import LLMService
from orchestrator.state import RequirementAssessment, Task, WorkflowState


def _deterministic_assessment(raw: str) -> RequirementAssessment:
	lowered = raw.lower()
	destructive = any(term in lowered for term in ("delete", "remove", "drop", "destroy", "purge"))
	ambiguous = any(term in lowered for term in ("popular", "faster", "better", "optimize")) and "clarification:" not in lowered
	brownfield = any(term in lowered for term in ("existing", "add ", "modify", "refactor")) or destructive
	requirement_type = "AMBIGUOUS" if ambiguous else "BROWNFIELD" if brownfield else "GREENFIELD"
	ambiguities = [
		"Define the measurable success metric and target threshold.",
		"Specify expected traffic, scale, and performance percentile.",
		"Clarify data retention, rollback, and operational constraints.",
	] if ambiguous else []
	if destructive:
		ambiguities.append("Confirm authorization, scope, audit requirements, and rollback for destructive data changes.")
	risk = "HIGH" if destructive or ambiguous else "MEDIUM" if brownfield else "LOW"
	normalized = raw.strip().rstrip(".") + "."
	return RequirementAssessment(
		normalized_requirement=normalized[:1].upper() + normalized[1:],
		requirement_type=requirement_type,
		acceptance_criteria=[
			"Define observable behavior and failure handling.",
			"Validate the change with automated tests and a release gate.",
		],
		ambiguities=ambiguities,
		assumptions=["The change targets the current local URL shortener repository."] if not ambiguities else [],
		risk_level=risk,
		confidence=0.72 if ambiguities else 0.88,
		security_considerations=["Validate inputs and preserve an auditable change history."] + (["Require explicit human approval before destructive execution."] if destructive else []),
		non_functional_requirements=["Backward compatibility", "Deterministic validation evidence", "Observable failure state"],
		impacted_components=["API contract", "service layer", "persistence", "tests", "documentation"],
		recommended_next_step="Resolve blocking ambiguities with the requestor." if ambiguities else "Proceed to architecture impact analysis.",
	)


def requirement_agent(state: WorkflowState) -> WorkflowState:
	raw = state.raw_requirement.strip()
	assessment = _deterministic_assessment(raw)
	llm = LLMService()
	if llm.available():
		try:
			assessment = llm.complete(f"Assess this software engineering requirement:\n\n{raw}")
			state.event("REQUIREMENTS", "llm_service", "structured_requirement_assessment", "PASSED", "OpenAI structured output")
		except Exception as exc:
			state.event("REQUIREMENTS", "llm_service", "structured_requirement_assessment", "FALLBACK", type(exc).__name__)
	state.assessment = assessment
	state.normalized_requirement = assessment.normalized_requirement
	state.requirement_type = assessment.requirement_type
	state.ambiguities = assessment.ambiguities
	state.assumptions = assessment.assumptions
	state.acceptance_criteria = assessment.acceptance_criteria
	state.risk_level = assessment.risk_level
	state.approval_status = "PENDING" if state.risk_level in {"MEDIUM", "HIGH"} else "NOT_REQUIRED"
	state.event("REQUIREMENTS", "requirement_agent", "normalize_requirement", "PASSED")
	return state


def architecture_agent(state: WorkflowState) -> WorkflowState:
	state.architecture_analysis = {
		"impacted_components": ["app/routes.py", "app/schemas.py", "app/url_service.py", "tests/"],
		"compatibility": "Existing URL records remain valid unless explicitly disabled.",
		"recommendation": "Keep business logic in the service layer and validate at the API boundary.",
	}
	state.decisions.append({"decision": "Use SQLite for the prototype", "reason": "Reproducible local persistence", "tradeoff": "Limited horizontal scale"})
	state.event("ARCHITECTURE", "architecture_agent", "analyze_impact", "PASSED")
	return state


def planning_agent(state: WorkflowState) -> WorkflowState:
	state.tasks = [
		Task(task_id="T1", description="Define and validate the API contract", validation="Pydantic schema tests"),
		Task(task_id="T2", description="Implement persistence and business behavior", dependencies=["T1"], validation="Service tests"),
		Task(task_id="T3", description="Add integration and security validation", dependencies=["T2"], validation="pytest and policy checks"),
		Task(task_id="T4", description="Document release readiness and limitations", dependencies=["T3"], validation="Documentation review"),
	]
	state.event("PLANNING", "planning_agent", "decompose_tasks", "PASSED")
	return state


def implementation_agent(state: WorkflowState) -> WorkflowState:
	state.changed_files = ["app/database.py", "app/models.py", "app/schemas.py", "app/url_service.py", "app/routes.py", "app/main.py"]
	for task in state.tasks:
		if task.task_id in {"T1", "T2"}:
			task.status = "complete"
	state.event("IMPLEMENTATION", "implementation_agent", "record_implementation", "PASSED")
	return state
