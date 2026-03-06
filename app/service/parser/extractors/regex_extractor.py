"""
Concrete extractor that relies on regular expressions + heuristics.

IMPORTANT:
  CVs come in wildly different layouts.  This extractor covers the
  most common patterns.  For production accuracy you would swap this
  out for an LLM-based or NER-based extractor — the interface stays
  the same thanks to BaseExtractor.
"""

from __future__ import annotations

import re
from typing import List, Optional, Tuple

from app.service.parser.models.cv_data import CVData, Education, Experience, Project
from .base_extractor import BaseExtractor


# ─── Section heading patterns ────────────────────────────────────────
_SECTION_PATTERNS: dict[str, re.Pattern] = {
    "education": re.compile(
        r"^[\s]*(?:education|academic|qualification|degree)s?\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "skills": re.compile(
        r"^[\s]*(?:skills|technical\s*skills|core\s*competenc|"
        r"technologies|tech\s*stack|proficienc|tools\s*(?:&|and)\s*technolog)",
        re.IGNORECASE | re.MULTILINE,
    ),
    "experience": re.compile(
        r"^[\s]*(?:experience|work\s*experience|employment|"
        r"professional\s*experience|career\s*history|work\s*history)",
        re.IGNORECASE | re.MULTILINE,
    ),
    "projects": re.compile(
        r"^[\s]*(?:projects?|personal\s*projects?|"
        r"academic\s*projects?|key\s*projects?|project\s*experience)",
        re.IGNORECASE | re.MULTILINE,
    ),
}

# ─── Contact-info patterns ────────────────────────────────────────────
_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[\s.-]?)?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}"
)
_LINKEDIN_RE = re.compile(r"linkedin\.com/in/[\w-]+", re.IGNORECASE)

# Common location markers
_LOCATION_RE = re.compile(
    r"(?:location|address|city|based\s*in)[:\s]*([^\n]+)",
    re.IGNORECASE,
)
# Fallback: city, STATE/Country pattern
_LOCATION_FALLBACK_RE = re.compile(
    r"\b([A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*,\s*[A-Z][\w\s]*)\b"
)

# Year pattern
_YEAR_RE = re.compile(r"(?:19|20)\d{2}")

# Degree keywords
_DEGREE_KEYWORDS = [
    "ph\.?d", "doctorate", "master", "m\.?s\.?c?", "m\.?a\.?",
    "m\.?b\.?a", "bachelor", "b\.?s\.?c?", "b\.?a\.?", "b\.?e\.?",
    "b\.?tech", "m\.?tech", "diploma", "associate", "a\.?s\.?",
    "high\s*school", "secondary", "intermediate", "matric",
    "certification", "certificate",
]
_DEGREE_RE = re.compile(
    r"\b(?:" + "|".join(_DEGREE_KEYWORDS) + r")[\w.\s]*",
    re.IGNORECASE,
)

# Skill-like tokens (rough: anything that looks like a tech word)
_SKILL_DELIMITERS = re.compile(r"[,;|•●◦▪▸►\-–—]|\n")

# Duration pattern  e.g.  Jan 2020 – Mar 2022 / 2019-2021 / (2 years)
_DURATION_RE = re.compile(
    r"(?:"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?"
    r"[\s,]*\d{4}\s*[-–—to]+\s*"
    r"(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?"
    r"[\s,]*\d{4}|present|current|now|ongoing)"
    r"|"
    r"\d{4}\s*[-–—to]+\s*(?:\d{4}|present|current|now|ongoing)"
    r")",
    re.IGNORECASE,
)


class RegexExtractor(BaseExtractor):
    """Regex / heuristic-based CV field extractor."""

    # ── public API ────────────────────────────────────────
    def extract(self, raw_text: str) -> CVData:
        cv = CVData(raw_text=raw_text)

        # 1. contact info (can appear anywhere, usually top)
        cv.email = self._find_email(raw_text)
        cv.phone_number = self._find_phone(raw_text)
        cv.full_name = self._find_name(raw_text, cv.email, cv.phone_number)
        cv.location = self._find_location(raw_text)

        # 2. split into sections
        sections = self._split_sections(raw_text)

        # 3. per-section extraction
        cv.education = self._extract_education(sections.get("education", ""))
        cv.skills = self._extract_skills(sections.get("skills", ""))
        cv.experience = self._extract_experience(sections.get("experience", ""))
        cv.projects = self._extract_projects(sections.get("projects", ""))

        # 4. If skills section was empty, try to pull skills from the full text
        if not cv.skills:
            cv.skills = self._extract_skills_fallback(raw_text)

        return cv

    # ── section splitting ─────────────────────────────────
    def _split_sections(self, text: str) -> dict[str, str]:
        """Find known section headings and slice the text accordingly."""
        markers: list[Tuple[int, str]] = []
        for section_name, pattern in _SECTION_PATTERNS.items():
            match = pattern.search(text)
            if match:
                markers.append((match.start(), section_name))

        markers.sort(key=lambda m: m[0])

        sections: dict[str, str] = {}
        for idx, (start, name) in enumerate(markers):
            # skip past the heading line itself
            heading_end = text.index("\n", start) + 1 if "\n" in text[start:] else start
            end = markers[idx + 1][0] if idx + 1 < len(markers) else len(text)
            sections[name] = text[heading_end:end].strip()

        return sections

    # ── contact info helpers ──────────────────────────────
    @staticmethod
    def _find_email(text: str) -> str:
        match = _EMAIL_RE.search(text)
        return match.group(0) if match else ""

    @staticmethod
    def _find_phone(text: str) -> str:
        match = _PHONE_RE.search(text)
        return match.group(0).strip() if match else ""

    @staticmethod
    def _find_name(text: str, email: str, phone: str) -> str:
        """
        Heuristic: the name is usually the very first non-empty line
        that is NOT an email / phone / URL.
        """
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            # skip lines that are obviously not names
            if "@" in line:
                continue
            if _PHONE_RE.fullmatch(line):
                continue
            if line.lower().startswith("http"):
                continue
            if "linkedin" in line.lower():
                continue
            # If the line is very long (> 60 chars) it's probably a summary
            if len(line) > 60:
                continue
            # Likely the candidate's name
            # Clean any stray special characters
            name = re.sub(r"[^\w\s.'-]", "", line).strip()
            if name:
                return name
        return ""

    @staticmethod
    def _find_location(text: str) -> str:
        match = _LOCATION_RE.search(text)
        if match:
            return match.group(1).strip()
        # look in the first 600 chars for city, country patterns
        head = text[:600]
        match = _LOCATION_FALLBACK_RE.search(head)
        if match:
            return match.group(1).strip()
        return ""

    # ── education extraction ──────────────────────────────
    def _extract_education(self, section: str) -> List[Education]:
        if not section:
            return []

        entries: List[Education] = []
        lines = [l.strip() for l in section.splitlines() if l.strip()]

        # Try to parse multi-line blocks or single-line entries
        current_block: list[str] = []
        for line in lines:
            # A new block starts if the line contains a degree keyword or a year
            if _DEGREE_RE.search(line) or _YEAR_RE.search(line):
                if current_block:
                    entries.append(self._parse_education_block(current_block))
                current_block = [line]
            else:
                current_block.append(line)

        if current_block:
            entries.append(self._parse_education_block(current_block))

        # deduplicate empty entries
        return [e for e in entries if e.degree or e.institution]

    @staticmethod
    def _parse_education_block(block: list[str]) -> Education:
        full = " | ".join(block)
        degree = ""
        institution = ""
        year = ""

        deg_match = _DEGREE_RE.search(full)
        if deg_match:
            degree = deg_match.group(0).strip()

        years = _YEAR_RE.findall(full)
        if years:
            year = years[-1]  # latest year (graduation)

        # institution: remove degree & year from the text; the rest is likely the institution
        remaining = full
        if degree:
            remaining = remaining.replace(degree, "")
        for y in years:
            remaining = remaining.replace(y, "")
        # clean up separators
        remaining = re.sub(r"[|,\-–—•]", " ", remaining).strip()
        remaining = re.sub(r"\s{2,}", " ", remaining).strip()
        if remaining:
            institution = remaining

        return Education(degree=degree, institution=institution, year=year)

    # ── skills extraction ─────────────────────────────────
    @staticmethod
    def _extract_skills(section: str) -> List[str]:
        if not section:
            return []
        # split by common delimiters
        tokens = _SKILL_DELIMITERS.split(section)
        skills = []
        for token in tokens:
            token = token.strip().strip("()").strip()
            # skip empties, pure numbers, or very long strings (sentences)
            if not token or token.isdigit() or len(token) > 50:
                continue
            # skip lines that look like section headers
            if any(
                token.lower().startswith(kw)
                for kw in ["experience", "education", "project", "summary"]
            ):
                continue
            skills.append(token)
        return list(dict.fromkeys(skills))  # dedupe, preserve order

    @staticmethod
    def _extract_skills_fallback(text: str) -> List[str]:
        """Pull a small set of well-known tech keywords from the full text."""
        known = [
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "C",
            "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala",
            "R", "MATLAB", "SQL", "NoSQL", "HTML", "CSS", "SASS",
            "React", "Angular", "Vue", "Svelte", "Next.js", "Nuxt",
            "Node.js", "Express", "Django", "Flask", "FastAPI",
            "Spring", "Spring Boot", ".NET", "ASP.NET",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP",
            "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
            "Git", "GitHub", "GitLab", "CI/CD", "Jenkins", "Terraform",
            "Linux", "Bash", "PowerShell",
            "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
            "Tableau", "Power BI", "Excel", "Figma", "Jira",
            "REST", "GraphQL", "gRPC", "Kafka", "RabbitMQ",
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
            "Agile", "Scrum", "Kanban",
        ]
        found = []
        for skill in known:
            # word-boundary search (case-insensitive for most, exact for short ones)
            if len(skill) <= 2:
                pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"
            else:
                pattern = rf"\b{re.escape(skill)}\b"
            if re.search(pattern, text, re.IGNORECASE):
                found.append(skill)
        return found

    # ── experience extraction ─────────────────────────────
    def _extract_experience(self, section: str) -> List[Experience]:
        if not section:
            return []

        entries: List[Experience] = []
        lines = [l.strip() for l in section.splitlines() if l.strip()]

        # Heuristic: a new experience entry starts when we see a duration pattern
        # or a line that looks like a role/title (short, may end with a date)
        blocks: list[list[str]] = []
        current: list[str] = []

        for line in lines:
            if _DURATION_RE.search(line) and current:
                # If the duration is in the same line as a previous block, merge
                if len(current) == 1:
                    current.append(line)
                    continue
                blocks.append(current)
                current = [line]
            else:
                current.append(line)
        if current:
            blocks.append(current)

        for block in blocks:
            entries.append(self._parse_experience_block(block))

        return [e for e in entries if e.role or e.company]

    @staticmethod
    def _parse_experience_block(block: list[str]) -> Experience:
        full = "\n".join(block)
        duration = ""
        dur_match = _DURATION_RE.search(full)
        if dur_match:
            duration = dur_match.group(0).strip()

        # First line is usually role at company or company - role
        first_line = block[0]
        role = ""
        company = ""

        # Try splitting by common separators
        for sep in [" at ", " @ ", " | ", " - ", " – ", " — ", ", "]:
            if sep in first_line:
                parts = first_line.split(sep, 1)
                role = parts[0].strip()
                company = parts[1].strip()
                break
        else:
            role = first_line.strip()

        # Clean duration out of role / company
        if duration:
            role = role.replace(duration, "").strip().strip("|()")
            company = company.replace(duration, "").strip().strip("|()")

        # Summary = rest of the lines joined
        summary_lines = block[1:] if len(block) > 1 else []
        summary = " ".join(l.strip() for l in summary_lines if l.strip())
        # trim to ~200 chars
        if len(summary) > 200:
            summary = summary[:197] + "..."

        return Experience(role=role, company=company, duration=duration, summary=summary)

    # ── projects extraction ───────────────────────────────
    def _extract_projects(self, section: str) -> List[Project]:
        if not section:
            return []

        entries: List[Project] = []
        lines = [l.strip() for l in section.splitlines() if l.strip()]

        # Heuristic: each project block starts with a "title" line
        # (often bold / short) followed by description lines
        blocks: list[list[str]] = []
        current: list[str] = []

        for line in lines:
            # New project if line looks like a heading (short, no sentence punctuation at end)
            is_heading = (
                len(line) < 80
                and not line.endswith(".")
                and not line[0].isdigit()
            ) or line.startswith(("•", "-", "●", "▪", "►"))

            if is_heading and current:
                blocks.append(current)
                current = [line]
            else:
                current.append(line)
        if current:
            blocks.append(current)

        for block in blocks:
            entries.append(self._parse_project_block(block))

        return [p for p in entries if p.name]

    def _parse_project_block(self, block: list[str]) -> Project:
        # Title: first line (cleaned of bullet chars)
        title = re.sub(r"^[\s•\-●▪►]+", "", block[0]).strip()
        # Collect any tech skills mentioned
        body = " ".join(block)
        skills = self._extract_skills_fallback(body)
        return Project(name=title, skills=skills)