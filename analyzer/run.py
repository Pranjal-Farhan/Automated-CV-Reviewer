import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cv_analyzer.analyzers.gemini_analyzer import GeminiAnalyzer
from cv_analyzer.formatters.terminal_formatter import TerminalFormatter

# ── Docker detection ──
RUNNING_IN_DOCKER = os.path.exists("/.dockerenv")
OUTPUT_DIR = "/app/output" if RUNNING_IN_DOCKER else "../output"

# ══════════════════════════════════════════
# MOCK DATA — For testing without parser
# ══════════════════════════════════════════
MOCK_RAW_TEXT = """
CHRISTINE SMITH
+1 (970) 333-3833
christine.smidth@mail.com
https://www.coolfreecv.com

Summary
My name is Christine Smith an expert Web and Graphic Designer.
I have over 7 years experience within the industry. My specialty is
in Adobe Photoshop, Illustrator, Branding and creating attractive
Responsive Websites using CSS, HTML, jQuery, Bootstrap and Wordpress.

Skills
Ability to turnaround artwork quickly on short notice.
Exceptional eye for and attention to detail.
Working knowledge of HTML5, CSS3, JQuery, PHP, XML.
Proficiency in Photoshop, Illustrator and InDesign.

Experience
GRAPHIC WEB DESIGNER - 05/2013 to 05/2019
LUNA, LOS ANGELES
Design & develop online brand creative pieces including landing pages.
Create comps for new and updated web pages.

Education
CALIFORNIA STATE UNIVERSITY, LOS ANGELES
Bachelor's Degree in Graphic Design
"""


def display_banner():
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║      🤖 CV ANALYZER SERVICE                         ║")
    print("║      Powered by Google Gemini 2.5 Flash             ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()


def analyze_raw(analyzer, formatter, raw_text, source):
    """Analyze raw text using Gemini."""
    
    print(f"📄 Raw text loaded: {len(raw_text)} characters")
    print("🤖 Sending raw text directly to Gemini...\n")

    metadata = {
        "Source File": source,
        "Mode": "Raw Text → Gemini (no regex)",
        "AI Model": analyzer.get_model_name(),
    }

    result = analyzer.analyze_raw_text(raw_text)

    if result.startswith("❌"):
        formatter.display_error(result)
    else:
        formatter.display(result, metadata)


def main():
    display_banner()

    arg_parser = argparse.ArgumentParser(
        description="Analyze CV using Gemini 2.5 Flash."
    )
    arg_parser.add_argument(
        "--test", action="store_true",
        help="Run with mock data."
    )
    arg_parser.add_argument(
        "--raw", type=str,
        help="Path to raw .txt file from parser."
    )

    args = arg_parser.parse_args()

    try:
        analyzer = GeminiAnalyzer()
        formatter = TerminalFormatter()
    except ValueError as e:
        print(e)
        sys.exit(1)

    if args.test:
        print("🧪 TEST MODE\n")
        analyze_raw(analyzer, formatter, MOCK_RAW_TEXT, "Mock Data")

    elif args.raw:
        if not os.path.exists(args.raw):
            print(f"❌ File not found: {args.raw}")
            sys.exit(1)

        with open(args.raw, "r", encoding="utf-8") as f:
            raw_text = f.read()

        analyze_raw(analyzer, formatter, raw_text, args.raw)

    else:
        print("Usage:")
        print("  python run.py --test")
        print("  python run.py --raw ../output/CV_pdfplumber_raw.txt")
        sys.exit(1)

    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()