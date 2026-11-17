"""Tests for the provider-independent LLM registry."""

import pytest

from app.llm.base import LLMProvider
from app.llm.registry import (
    LLMProviderNotConfiguredError,
    get_llm_provider,
    register_llm_provider,
)


class FakeProvider(LLMProvider):
    def generate(
        self, *, system_prompt: str, user_prompt: str, temperature: float = 0.2
    ) -> str:
        return f"{system_prompt}:{user_prompt}:{temperature}"


def test_disabled_provider_returns_none():
    assert get_llm_provider("none") is None


def test_registered_provider_can_be_resolved():
    register_llm_provider("test-provider", FakeProvider)

    provider = get_llm_provider("TEST-PROVIDER")

    assert isinstance(provider, FakeProvider)
    assert provider.generate(system_prompt="system", user_prompt="hello") == "system:hello:0.2"


def test_unknown_provider_raises_clear_error():
    with pytest.raises(LLMProviderNotConfiguredError, match="not registered"):
        get_llm_provider("unknown-provider")
