"""
Factory that creates parser instances by name.

Open/Closed: register new parsers via `register()` — no need to touch
existing code.
"""

from __future__ import annotations

from typing import Dict, Type

from app.service.parser.parsers.base_parser import BaseParser
from app.service.parser.parsers.pypdf_parser import PyPDFParser
from app.service.parser.parsers.pdfplumber_parser import PDFPlumberParser
from app.service.parser.parsers.pdfminer_parser import PDFMinerParser


class ParserFactory:
    """Creates BaseParser instances by name."""

    _registry: Dict[str, Type[BaseParser]] = {
        "pypdf": PyPDFParser,
        "pdfplumber": PDFPlumberParser,
        "pdfminer": PDFMinerParser,
    }

    # ── public API ────────────────────────────────────────
    @classmethod
    def create(cls, parser_name: str) -> BaseParser:
        """Return a parser instance.  Raises ValueError for unknown names."""
        key = parser_name.strip().lower()
        if key not in cls._registry:
            available = ", ".join(sorted(cls._registry))
            raise ValueError(
                f"Unknown parser '{parser_name}'. Available: {available}"
            )
        return cls._registry[key]()

    @classmethod
    def register(cls, name: str, parser_class: Type[BaseParser]) -> None:
        """Register a new parser at runtime (for future extensions)."""
        cls._registry[name.strip().lower()] = parser_class

    @classmethod
    def available(cls) -> list[str]:
        return sorted(cls._registry)