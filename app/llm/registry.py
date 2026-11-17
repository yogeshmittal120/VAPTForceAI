"""Registry for pluggable LLM provider adapters."""

from collections.abc import Callable

from app.llm.base import LLMProvider

ProviderFactory = Callable[[], LLMProvider]
_provider_factories: dict[str, ProviderFactory] = {}


class LLMProviderNotConfiguredError(RuntimeError):
    """Raised when a requested provider has no registered adapter."""


def register_llm_provider(name: str, factory: ProviderFactory) -> None:
    """Register a provider factory under a normalized provider name."""
    normalized_name = name.strip().lower()
    if not normalized_name:
        raise ValueError("Provider name cannot be empty")
    _provider_factories[normalized_name] = factory


def get_llm_provider(name: str = "none") -> LLMProvider | None:
    """Return a provider instance, or None when LLM use is disabled."""
    normalized_name = name.strip().lower()
    if normalized_name in {"", "none", "disabled"}:
        return None
    factory = _provider_factories.get(normalized_name)
    if factory is None:
        available = ", ".join(sorted(_provider_factories)) or "none"
        raise LLMProviderNotConfiguredError(
            f"LLM provider '{normalized_name}' is not registered. "
            f"Registered providers: {available}"
        )
    return factory()
