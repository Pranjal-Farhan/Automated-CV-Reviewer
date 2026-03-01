from .base_formatter import BaseFormatter


class TerminalFormatter(BaseFormatter):

    def display(self, analysis_text: str, metadata: dict) -> None:

        print("\n" + "═" * 60)
        print("  📋 CV ANALYSIS REPORT")
        print("═" * 60)

        if metadata:
            print("\n📂 SOURCE INFO:")
            print("─" * 40)
            for key, value in metadata.items():
                print(f"   {key:<20}: {value}")
            print("─" * 40)

        print("\n🤖 GEMINI ANALYSIS:")
        print("═" * 60)
        print(analysis_text)
        print("═" * 60)

    def display_error(self, error_msg: str) -> None:
        print("\n" + "!" * 60)
        print(f"  ❌ ERROR: {error_msg}")
        print("!" * 60)