"""
Abstract extractor interface.
"""

from abc import ABC, abstractmethod

from cv_parser.models.cv_data import CVData


class BaseExtractor(ABC):
    """Turn raw text into a structured CVData object."""

    @abstractmethod
    def extract(self, raw_text: str) -> CVData:
        ...