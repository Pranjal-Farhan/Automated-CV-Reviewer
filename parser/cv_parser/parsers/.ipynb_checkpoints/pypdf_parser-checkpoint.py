#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""Concrete parser: uses the *pypdf* library."""

from pathlib import Path
from pypdf import PdfReader

from .base_parser import BaseParser


class PyPDFParser(BaseParser):

    @property
    def name(self) -> str:
        return "pypdf"

    def extract_text(self, file_path: Path) -> str:
        path = self._validate_path(file_path)
        reader = PdfReader(str(path))
        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        return "\n".join(pages_text)

