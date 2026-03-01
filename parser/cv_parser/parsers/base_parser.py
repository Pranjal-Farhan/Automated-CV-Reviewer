"""
Abstract base class that every PDF text-extractor must implement.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseParser(ABC):
    """Interface: extract raw text from a PDF file."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable parser name (used in logs / output)."""
        ...

    @abstractmethod
    def extract_text(self, file_path: Path) -> str:
        """
        Read *file_path* and return the full plain-text content.
        Raises FileNotFoundError if the path is invalid.
        """
        ...

    # ── shared guard ──────────────────────────────────────
    @staticmethod
    def _validate_path(file_path: Path) -> Path:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a .pdf file, got: {path.suffix}")
        return path

