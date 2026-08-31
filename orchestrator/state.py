from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


class WorkflowEvent(BaseModel):
	timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
	stage: str
	agent: str
	action: str
	status: str
	attempt: int = 1
	detail: str | None = None


class RequirementAssessment(BaseModel):
	normalized_requirement: str
	requirement_type: str
	acceptance_criteria: list[str]
	ambiguities: list[str]
	assumptions: list[str]
	risk_level: str
	confidence: float = Field(ge=0, le=1)
	security_considerations: list[str] = []
	non_functional_requirements: list[str] = []
	impacted_components: list[str] = []
	recommended_next_step: str
	source: str = "deterministic"


class Task(BaseModel):
	task_id: str
	description: str
	dependencies: list[str] = []
	status: Literal["pending", "complete"] = "pending"
	risk: str = "LOW"
	validation: str


class WorkflowState(BaseModel):
	workflow_id: str
	status: str = "RUNNING"
	current_stage: str = "REQUIREMENTS"
	current_agent: str = "Requirement Agent"
	raw_requirement: str
	requirement_version: int = 1
	normalized_requirement: str = ""
	requirement_type: str = ""
	acceptance_criteria: list[str] = []
	assessment: RequirementAssessment | None = None
	node_statuses: dict[str, str] = {}
	ambiguities: list[str] = []
	assumptions: list[str] = []
	risk_level: str = "LOW"
	architecture_analysis: dict[str, Any] = {}
	tasks: list[Task] = []
	changed_files: list[str] = []
	test_results: dict[str, Any] = {}
	security_results: dict[str, Any] = {}
	retry_count: int = 0
	rollback_count: int = 0
	approval_status: str = "NOT_REQUIRED"
	approval_identity: str | None = None
	decisions: list[dict[str, str]] = []
	events: list[WorkflowEvent] = []
	started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
	completed_at: datetime | None = None

	def event(self, stage: str, agent: str, action: str, status: str, detail: str | None = None) -> None:
		self.events.append(WorkflowEvent(stage=stage, agent=agent, action=action, status=status, detail=detail))
