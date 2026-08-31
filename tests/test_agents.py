from orchestrator.agents import requirement_agent
from orchestrator.state import WorkflowState


def test_ambiguous_requirement_is_explicitly_detected() -> None:
	state = WorkflowState(workflow_id="WF-TEST", raw_requirement="Make popular URLs faster")
	requirement_agent(state)
	assert state.requirement_type == "AMBIGUOUS"
	assert state.risk_level == "HIGH"
	assert state.ambiguities


def test_assessment_contains_reviewable_engineering_detail() -> None:
	state = WorkflowState(workflow_id="WF-TEST", raw_requirement="Add expiration support to existing URLs")
	requirement_agent(state)
	assert state.assessment is not None
	assert state.assessment.confidence > 0
	assert state.assessment.acceptance_criteria
	assert state.assessment.impacted_components
	assert state.assessment.recommended_next_step
