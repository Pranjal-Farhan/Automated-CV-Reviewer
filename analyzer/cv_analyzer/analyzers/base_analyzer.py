from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):
    """Abstract base for all LLM analyzers."""

    @abstractmethod
    def analyze_raw_text(self, raw_text: str) -> str:
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        pass