"""Concrete parser: uses the *pdfminer.six* library."""

from pathlib import Path
from pdfminer.high_level import extract_text as pdfminer_extract

from .base_parser import BaseParser


class PDFMinerParser(BaseParser):

    @property
    def name(self) -> str:
        return "pdfminer"

    def extract_text(self, file_path: Path) -> str:
        path = self._validate_path(file_path)
        text = pdfminer_extract(str(path))
        return text if text else ""
