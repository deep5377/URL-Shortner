from datetime import datetime, timezone
from threading import Lock
from typing import TypedDict
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.schemas import ApprovalRequest, ClarificationRequest, WorkflowCreate
from orchestrator.agents import architecture_agent, implementation_agent, planning_agent, requirement_agent
from orchestrator.policies import MAX_RETRIES, can_release
from orchestrator.state import WorkflowState
from orchestrator.tools import run_security_checks, run_tests

try:
	from langgraph.graph import END, START, StateGraph
except ImportError:  # Local fallback keeps the prototype runnable if optional orchestration dependencies are unavailable.
	END = START = StateGraph = None

workflow_router = APIRouter()
_workflows: dict[str, WorkflowState] = {}
_checkpoints: dict[str, WorkflowState] = {}
_lock = Lock()


class GraphInput(TypedDict):
	workflow: WorkflowState


def _requirement_node(data: GraphInput) -> GraphInput:
	state = data["workflow"]
	state.node_statuses = {"REQUIREMENTS": "RUNNING"}
	state.current_agent = "Requirement Agent"
	requirement_agent(state)
	return data


def _architecture_node(data: GraphInput) -> GraphInput:
	state = data["workflow"]
	state.node_statuses.update({"REQUIREMENTS": "PASSED", "ARCHITECTURE": "RUNNING", "RISK": "RUNNING"})
	state.current_stage = "ARCHITECTURE"
	state.current_agent = "Architecture Agent / Policy Engine"
	architecture_agent(state)
	state.node_statuses.update({"ARCHITECTURE": "PASSED", "RISK": "PASSED"})
	return data


def _planning_node(data: GraphInput) -> GraphInput:
	state = data["workflow"]
	planning_agent(state)
	state.node_statuses["PLANNING"] = "PASSED"
	return data


def _implementation_node(data: GraphInput) -> GraphInput:
	state = data["workflow"]
	implementation_agent(state)
	state.node_statuses["IMPLEMENTATION"] = "PASSED"
	return data


def _validation_node(data: GraphInput) -> GraphInput:
	state = data["workflow"]
	state.current_stage = "VALIDATION"
	state.current_agent = "Test / Diagnosis Agent"
	state.node_statuses.update({"TESTS": "RUNNING", "SECURITY": "RUNNING"})
	state.test_results = run_tests()
	state.event("VALIDATION", "test_tool", "run_tests", "PASSED" if state.test_results["passed"] else "FAILED")
	state.security_results = run_security_checks()
	state.event("VALIDATION", "security_tool", "run_security_checks", "PASSED")
	state.node_statuses.update({"TESTS": "PASSED" if state.test_results["passed"] else "FAILED", "SECURITY": "PASSED" if state.security_results["passed"] else "FAILED"})
	return data


def _route_after_requirements(data: GraphInput) -> str:
	return "stop" if data["workflow"].requirement_type == "AMBIGUOUS" else "architecture"


def _build_langgraph():
	if StateGraph is None:
		return None
	graph = StateGraph(GraphInput)
	graph.add_node("requirements", _requirement_node)
	graph.add_node("architecture", _architecture_node)
	graph.add_node("planning", _planning_node)
	graph.add_node("implementation", _implementation_node)
	graph.add_node("validation", _validation_node)
	graph.add_edge(START, "requirements")
	graph.add_conditional_edges("requirements", _route_after_requirements, {"stop": END, "architecture": "architecture"})
	graph.add_edge("architecture", "planning")
	graph.add_edge("planning", "implementation")
	graph.add_edge("implementation", "validation")
	graph.add_edge("validation", END)
	return graph.compile()


compiled_graph = _build_langgraph()


def execute_workflow(state: WorkflowState) -> WorkflowState:
	if compiled_graph is not None:
		compiled_graph.invoke({"workflow": state})
	else:
		_requirement_node({"workflow": state})
	if state.requirement_type == "AMBIGUOUS":
		state.node_statuses["REQUIREMENTS"] = "SAFE_STOP"
		state.status = "SAFE_STOP"
		state.current_stage = "REQUIREMENTS"
		state.event("GOVERNANCE", "policy_engine", "safe_stop", "BLOCKED", "Blocking ambiguity requires human clarification")
		return state
	if compiled_graph is None:
		_architecture_node({"workflow": state})
		_planning_node({"workflow": state})
		_implementation_node({"workflow": state})
		_validation_node({"workflow": state})
	if not state.test_results["passed"]:
		state.retry_count += 1
		if state.retry_count >= MAX_RETRIES:
			state.status = "SAFE_STOP"
			state.event("GOVERNANCE", "policy_engine", "retry_exhausted", "BLOCKED")
		else:
			state.status = "RETRY_REQUIRED"
		return state
	if state.approval_status == "PENDING":
		state.node_statuses["APPROVAL"] = "WAITING_APPROVAL"
		state.status = "AWAITING_APPROVAL"
		state.current_stage = "APPROVAL"
		state.event("APPROVAL", "policy_engine", "request_human_approval", "PENDING")
		return state
	state.status = "RELEASE_READY" if can_release(state) else "SAFE_STOP"
	state.node_statuses["RELEASE"] = state.status
	state.current_stage = "RELEASE"
	state.completed_at = datetime.now(timezone.utc)
	state.event("RELEASE", "release_agent", "evaluate_release_readiness", state.status)
	return state


@workflow_router.post("/api/v1/workflows", response_model=WorkflowState, status_code=201)
def start_workflow(payload: WorkflowCreate) -> WorkflowState:
	state = WorkflowState(workflow_id=f"WF-{uuid4().hex[:8].upper()}", raw_requirement=payload.requirement)
	with _lock:
		_checkpoints[state.workflow_id] = state.model_copy(deep=True)
		_workflows[state.workflow_id] = execute_workflow(state)
	return _workflows[state.workflow_id]


@workflow_router.get("/api/v1/workflows/{workflow_id}", response_model=WorkflowState)
def workflow_status(workflow_id: str) -> WorkflowState:
	if workflow_id not in _workflows:
		raise HTTPException(status_code=404, detail="workflow not found")
	return _workflows[workflow_id]


@workflow_router.get("/api/v1/workflows", response_model=list[WorkflowState])
def workflow_history() -> list[WorkflowState]:
	return sorted(_workflows.values(), key=lambda workflow: workflow.started_at, reverse=True)


@workflow_router.get("/api/v1/workflows/{workflow_id}/events")
def workflow_events(workflow_id: str) -> list[dict[str, object]]:
	return [event.model_dump(mode="json") for event in workflow_status(workflow_id).events]


@workflow_router.post("/api/v1/workflows/{workflow_id}/clarify", response_model=WorkflowState)
def clarify_workflow(workflow_id: str, payload: ClarificationRequest) -> WorkflowState:
	state = workflow_status(workflow_id)
	if state.status != "SAFE_STOP" or state.requirement_type != "AMBIGUOUS":
		raise HTTPException(status_code=409, detail="workflow is not awaiting clarification")
	state.raw_requirement = f"{state.raw_requirement}\nClarification: {payload.clarification}"
	state.requirement_version += 1
	state.status = "RUNNING"
	state.events.append(state.events[-1].model_copy(update={"action": "clarification_received", "status": "PASSED", "detail": f"Requirement version {state.requirement_version}"}))
	return execute_workflow(state)


@workflow_router.post("/api/v1/workflows/{workflow_id}/rollback", response_model=WorkflowState)
def rollback_workflow(workflow_id: str) -> WorkflowState:
	state = workflow_status(workflow_id)
	checkpoint = _checkpoints.get(workflow_id)
	if checkpoint is None:
		raise HTTPException(status_code=409, detail="no rollback checkpoint exists")
	restored = checkpoint.model_copy(deep=True)
	restored.rollback_count = state.rollback_count + 1
	restored.status = "SAFE_STOP"
	restored.current_stage = "GOVERNANCE"
	restored.current_agent = "Policy Engine"
	restored.event("GOVERNANCE", "policy_engine", "rollback_workflow", "PASSED", "Restored pre-execution workflow checkpoint; human review required")
	_workflows[workflow_id] = restored
	return restored


@workflow_router.get("/api/v1/metrics")
def workflow_metrics() -> dict[str, float | int]:
	workflows = list(_workflows.values())
	total = len(workflows)
	completed = [workflow for workflow in workflows if workflow.completed_at is not None]
	durations = [
		(workflow.completed_at - workflow.started_at).total_seconds()
		for workflow in completed
		if workflow.completed_at is not None
	]
	return {
		"total_workflows": total,
		"successful_workflows": sum(workflow.status == "RELEASE_READY" for workflow in workflows),
		"running_workflows": sum(workflow.status in {"RUNNING", "RETRY_REQUIRED"} for workflow in workflows),
		"approval_required": sum(workflow.status == "AWAITING_APPROVAL" for workflow in workflows),
		"safe_stops": sum(workflow.status == "SAFE_STOP" for workflow in workflows),
		"retry_count": sum(workflow.retry_count for workflow in workflows),
		"rollback_count": sum(workflow.rollback_count for workflow in workflows),
		"human_interventions": sum(workflow.approval_status in {"APPROVED", "REJECTED"} for workflow in workflows),
		"average_duration_seconds": sum(durations) / len(durations) if durations else 0,
	}


@workflow_router.post("/api/v1/workflows/{workflow_id}/approve", response_model=WorkflowState)
def approve_workflow(workflow_id: str, payload: ApprovalRequest) -> WorkflowState:
	state = workflow_status(workflow_id)
	if state.status != "AWAITING_APPROVAL":
		raise HTTPException(status_code=409, detail="workflow is not awaiting approval")
	state.approval_status = "APPROVED"
	state.approval_identity = payload.approver
	state.event("APPROVAL", payload.approver, "approve_workflow", "APPROVED", payload.reason)
	state.status = "RELEASE_READY" if can_release(state) else "SAFE_STOP"
	state.current_stage = "RELEASE"
	state.completed_at = datetime.now(timezone.utc)
	state.event("RELEASE", "release_agent", "evaluate_release_readiness", state.status)
	return state


@workflow_router.post("/api/v1/workflows/{workflow_id}/reject", response_model=WorkflowState)
def reject_workflow(workflow_id: str, payload: ApprovalRequest) -> WorkflowState:
	state = workflow_status(workflow_id)
	if state.status != "AWAITING_APPROVAL":
		raise HTTPException(status_code=409, detail="workflow is not awaiting approval")
	state.approval_status = "REJECTED"
	state.approval_identity = payload.approver
	state.status = "SAFE_STOP"
	state.current_stage = "GOVERNANCE"
	state.event("APPROVAL", payload.approver, "reject_workflow", "REJECTED", payload.reason)
	return state
