"""
Data models representing structured CV information.
Single Responsibility: Only holds data, no logic.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Education:
    """Represents one education entry."""
    degree: str = ""
    institution: str = ""
    year: str = ""


@dataclass
class Experience:
    """Represents one work-experience entry."""
    role: str = ""
    company: str = ""
    duration: str = ""
    summary: str = ""


@dataclass
class Project:
    """Represents one project entry with its associated skills."""
    name: str = ""
    skills: List[str] = field(default_factory=list)


@dataclass
class CVData:
    """
    Top-level model that holds every piece of information
    extracted from a CV / résumé.
    """
    full_name: str = ""
    phone_number: str = ""
    email: str = ""
    location: str = ""
    education: List[Education] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    raw_text: str = ""                       # kept for debugging / re-processing
    parser_used: str = ""                    # which parser produced the text

    # ── helpers ────────────────────────────────────────────
    def to_dict(self) -> dict:
        """Convert to a plain dictionary (excludes raw_text for cleanliness)."""
        data = asdict(self)
        data.pop("raw_text", None)           # raw text is bulky; drop it
        return data

    def to_json(self, indent: int = 2) -> str:
        """Serialize to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @property
    def total_skills(self) -> int:
        return len(self.skills)

    @property
    def total_projects(self) -> int:
        return len(self.projects)