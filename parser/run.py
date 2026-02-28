#!/usr/bin/env python3
"""
CV Parser — Entry Point
=======================
Usage:
    python run.py <path_to_cv.pdf>                  # uses all 3 parsers
    python run.py <path_to_cv.pdf> --parser pypdf   # use a specific parser
    python run.py <path_to_cv.pdf> --parser pdfplumber
    python run.py <path_to_cv.pdf> --parser pdfminer

Outputs land in the ./output/ folder.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cv_parser.factory.parser_factory import ParserFactory
from cv_parser.extractors.regex_extractor import RegexExtractor
from cv_parser.formatters.json_formatter import JSONFormatter


def parse_with(parser_name: str, pdf_path: Path, extractor, formatter):
    """Run one parser end-to-end and display + save results."""
    print(f"\n{'='*60}")
    print(f"  PARSER: {parser_name.upper()}")
    print(f"{'='*60}")

    try:
        parser = ParserFactory.create(parser_name)
        raw_text = parser.extract_text(pdf_path)

        if not raw_text.strip():
            print(f"  ⚠️  {parser_name} returned empty text. Skipping.\n")
            return

        cv_data = extractor.extract(raw_text)
        cv_data.parser_used = parser_name

        # Display
        print(formatter.format(cv_data))

        # Save
        stem = pdf_path.stem
        out_path = Path("../output") / f"{stem}_{parser_name}"
        formatter.to_file(cv_data, str(out_path))

        raw_text_path = Path("../output") / f"{stem}_{parser_name}_raw.txt"
        with open(raw_text_path, "w", encoding="utf-8") as f:
            f.write(raw_text)
        print(f"  ✅ Raw text saved → {raw_text_path}")

    except Exception as exc:
        print(f"  ❌ Error with {parser_name}: {exc}\n")

def main():
    arg_parser = argparse.ArgumentParser(
        description="Parse a CV/Résumé PDF into structured JSON."
    )
    arg_parser.add_argument(
        "pdf", type=str, help="Path to the CV PDF file."
    )
    arg_parser.add_argument(
        "--parser", "-p",
        type=str,
        default="all",
        choices=["all"] + ParserFactory.available(),
        help="Which parser to use (default: all).",
    )

    args = arg_parser.parse_args()

    # Check both the raw path and the /app/input/ mounted path
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        # Try looking in the mounted input directory
        mounted_path = Path("/app/input") / pdf_path.name
        if mounted_path.exists():
            pdf_path = mounted_path
        else:
            print(f"❌ File not found: {pdf_path}")
            print(f"   Also checked: {mounted_path}")
            sys.exit(1)

    extractor = RegexExtractor()
    formatter = JSONFormatter()

    if args.parser == "all":
        for name in ParserFactory.available():
            parse_with(name, pdf_path, extractor, formatter)
    else:
        parse_with(args.parser, pdf_path, extractor, formatter)

    print("\n✅ Done! Check the ./output/ folder.\n")

if __name__ == "__main__":
    main()