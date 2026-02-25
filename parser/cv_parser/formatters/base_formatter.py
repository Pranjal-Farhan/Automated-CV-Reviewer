"""Abstract formatter interface — Open/Closed, Interface Segregation."""

from abc import ABC, abstractmethod
from cv_parser.models.cv_data import CVData


class BaseFormatter(ABC):

    @abstractmethod
    def format(self, cv: CVData) -> str:
        """Return a human-readable representation."""
        ...

    @abstractmethod
    def to_file(self, cv: CVData, output_path: str) -> None:
        """Persist the formatted output to disk."""
        ...