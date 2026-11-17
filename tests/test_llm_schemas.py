"""Tests for shared LLM request and response schemas."""

import pytest
from pydantic import ValidationError

from app.llm.schemas import LLMRequest, LLMResponse


def test_llm_request_uses_defaults():
    request = LLMRequest(system_prompt="You are helpful", user_prompt="Hello")

    assert request.temperature == 0.2
    assert request.model is None


def test_llm_request_rejects_temperature_outside_range():
    with pytest.raises(ValidationError):
        LLMRequest(
            system_prompt="System",
            user_prompt="Question",
            temperature=1.5,
        )


def test_llm_request_rejects_empty_prompts():
    with pytest.raises(ValidationError):
        LLMRequest(system_prompt="", user_prompt="Question")


def test_llm_response_accepts_usage_metadata():
    response = LLMResponse(
        content="Potential SQL injection",
        model="anthropic.claude-sonnet-5-5",
        input_tokens=120,
        output_tokens=35,
    )

    assert response.input_tokens == 120
    assert response.output_tokens == 35


def test_llm_response_allows_unknown_token_usage():
    response = LLMResponse(
        content="Analysis complete",
        model="example-model",
    )

    assert response.input_tokens is None
    assert response.output_tokens is None
