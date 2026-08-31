from datetime import datetime
from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, Field


class URLCreate(BaseModel):
	url: AnyHttpUrl
	expires_at: datetime | None = None


class URLResponse(BaseModel):
	short_code: str
	short_url: str
	original_url: str
	expires_at: datetime | None = None
	is_active: bool
	click_count: int


class AnalyticsResponse(BaseModel):
	short_code: str
	click_count: int


class WorkflowCreate(BaseModel):
	requirement: str = Field(min_length=5, max_length=5000)
	scenario: Literal["greenfield", "brownfield", "ambiguous"] | None = None


class ApprovalRequest(BaseModel):
	approver: str = Field(min_length=1, max_length=120)
	reason: str | None = Field(default=None, max_length=1000)


class ClarificationRequest(BaseModel):
	clarification: str = Field(min_length=5, max_length=5000)
