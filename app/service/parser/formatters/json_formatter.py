"""
Concrete formatter: JSON output + the pretty-printed display
the user requested.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.service.parser.models.cv_data import CVData
from .base_formatter import BaseFormatter


class JSONFormatter(BaseFormatter):

    # ── formatted display string ──────────────────────────
    def format(self, cv: CVData) -> str:
        sep = "─" * 50

        lines: list[str] = []

        # ── Candidate Info ──
        lines.append(f"\n{sep}")
        lines.append("📌 CANDIDATE INFORMATION")
        lines.append(sep)
        lines.append(f"Full Name       : {cv.full_name or 'N/A'}")
        lines.append(f"Phone Number    : {cv.phone_number or 'N/A'}")
        lines.append(f"Email           : {cv.email or 'N/A'}")
        lines.append(f"Location        : {cv.location or 'N/A'}")

        # ── Education ──
        lines.append(f"\n{sep}")
        lines.append("🎓 EDUCATION")
        lines.append(sep)
        if cv.education:
            for edu in cv.education:
                lines.append(
                    f"- {edu.degree or 'N/A'} | "
                    f"{edu.institution or 'N/A'} | "
                    f"{edu.year or 'N/A'}"
                )
        else:
            lines.append("  No education entries found.")

        # ── Skills ──
        lines.append(f"\n{sep}")
        lines.append("🛠 GENERAL SKILLS")
        lines.append(sep)
        lines.append(", ".join(cv.skills) if cv.skills else "  No skills found.")

        # ── Experience ──
        lines.append(f"\n{sep}")
        lines.append("💼 EXPERIENCE SUMMARY")
        lines.append(sep)
        if cv.experience:
            for exp in cv.experience:
                header = f"- {exp.role or 'N/A'}"
                if exp.company:
                    header += f" at {exp.company}"
                if exp.duration:
                    header += f" ({exp.duration})"
                lines.append(header)
                if exp.summary:
                    lines.append(f"  Summary: {exp.summary}")
        else:
            lines.append("  No experience entries found.")

        # ── Projects ──
        lines.append(f"\n{sep}")
        lines.append("🚀 PROJECTS & PROJECT SKILLS")
        lines.append(sep)
        if cv.projects:
            for proj in cv.projects:
                skills_str = ", ".join(proj.skills) if proj.skills else "N/A"
                lines.append(f"- {proj.name}: [{skills_str}]")
        else:
            lines.append("  No Projects Found")

        # ── Quick Summary ──
        lines.append(f"\n{sep}")
        lines.append("📊 QUICK SUMMARY")
        lines.append(sep)
        lines.append(f"Total Skills Found        : {cv.total_skills}")
        lines.append(f"Total Projects Found      : {cv.total_projects}")
        lines.append(f"Parser Used               : {cv.parser_used}")
        lines.append(sep)

        return "\n".join(lines)

    # ── save to file ──────────────────────────────────────
    def to_file(self, cv: CVData, output_path: str) -> None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write JSON
        json_path = path.with_suffix(".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(cv.to_dict(), f, indent=2, ensure_ascii=False)

        # Write the pretty-printed text too
        txt_path = path.with_suffix(".txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(self.format(cv))

        print(f"  ✅ JSON saved  → {json_path}")
        print(f"  ✅ Text saved  → {txt_path}")