"""Abstract interface implemented by future LLM provider adapters."""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Common contract so application services do not depend on one vendor."""

    @abstractmethod
    def generate(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
    ) -> str:
        """Generate a text response from the configured model."""
        raise NotImplementedError
