from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class ProjectSkill:
    name: str = ""
    skills: List[str] = field(default_factory=list)

    def __str__(self):
        return f"{self.name}: [{', '.join(self.skills)}]"


@dataclass
class AnalysisResult:
    full_name: str = "Not Found"
    phone_number: str = "Not Found"
    email: str = "Not Found"
    location: str = "Not Found"
    education: List[dict] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    experience: List[dict] = field(default_factory=list)
    projects: List[ProjectSkill] = field(default_factory=list)
    parser_used: str = ""
    model_used: str = ""