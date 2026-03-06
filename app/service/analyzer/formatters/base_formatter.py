from abc import ABC, abstractmethod


class BaseFormatter(ABC):

    @abstractmethod
    def display(self, analysis_text: str, metadata: dict) -> None:
        pass