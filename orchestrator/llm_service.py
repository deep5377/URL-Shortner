import os
from typing import Any

from openai import OpenAI

from orchestrator.state import RequirementAssessment


class LLMService:
	"""Centralized optional LLM boundary. Local workflows use deterministic agents."""

	def __init__(self) -> None:
		self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

	def available(self) -> bool:
		return bool(os.getenv("OPENAI_API_KEY")) and os.getenv("USE_LLM", "false").lower() == "true"

	def complete(self, prompt: str) -> Any:
		if not self.available():
			raise RuntimeError("LLM is disabled; set OPENAI_API_KEY and USE_LLM=true to enable it")
		client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], timeout=8.0, max_retries=1)
		response = client.chat.completions.parse(
			model=self.model,
			messages=[
				{"role": "system", "content": "You are a senior product engineer. Assess requirements conservatively. Never invent confirmed facts; put uncertainty in ambiguities or assumptions."},
				{"role": "user", "content": prompt},
			],
			response_format=RequirementAssessment,
		)
		parsed = response.choices[0].message.parsed
		if parsed is None:
			raise ValueError("LLM returned no structured requirement assessment")
		parsed.source = "openai"
		return parsed
