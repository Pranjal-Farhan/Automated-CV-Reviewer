#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""Concrete parser: uses the *pdfplumber* library."""

from pathlib import Path
import pdfplumber

from .base_parser import BaseParser


class PDFPlumberParser(BaseParser):

    @property
    def name(self) -> str:
        return "pdfplumber"

    def extract_text(self, file_path: Path) -> str:
        path = self._validate_path(file_path)
        pages_text = []
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
        return "\n".join(pages_text)

