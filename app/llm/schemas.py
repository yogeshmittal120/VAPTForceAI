"""Shared request and response schemas for all LLM providers."""

from pydantic import BaseModel, ConfigDict, Field


class LLMRequest(BaseModel):
    """Provider-neutral input accepted by the LLM service."""

    model_config = ConfigDict(extra="forbid")

    system_prompt: str = Field(min_length=1)
    user_prompt: str = Field(min_length=1)
    temperature: float = Field(default=0.2, ge=0.0, le=1.0)
    model: str | None = Field(default=None, min_length=1)


class LLMResponse(BaseModel):
    """Normalized output returned by every LLM provider adapter."""

    model_config = ConfigDict(extra="forbid")

    content: str
    model: str = Field(min_length=1)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
