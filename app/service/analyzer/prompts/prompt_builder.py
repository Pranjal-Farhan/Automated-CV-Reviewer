class PromptBuilder:

    @staticmethod
    def build_raw_text_prompt(raw_text: str) -> str:

        return f"""
You are an expert CV/Resume Analyzer. I will give you RAW TEXT 
extracted from a PDF file. No preprocessing has been done.

The text may be messy because:
- Multi-column layouts may mix text from different sections
- Headers and content might be jumbled
- Some text might be out of order

YOUR TASK:
Despite the messy text, intelligently extract and organize ALL 
information into a clean, structured JSON format.

RULES:
1. Extract ONLY what you can find. Do NOT invent data.
2. If something is not found, use null for single values or empty arrays for lists.
3. Be smart about multi-column text — reconstruct the meaning.
4. Respond with ONLY valid JSON. No markdown code blocks. No extra text before or after.
5. Do NOT wrap the response in ```json``` or any markdown formatting.

RESPOND WITH THIS EXACT JSON STRUCTURE:

{{
  "candidate_info": {{
    "name": "Full Name or null",
    "email": "email@example.com or null",
    "phone": "phone number or null",
    "location": "city/country or null",
    "linkedin": "LinkedIn URL or null",
    "website": "website URL or null"
  }},
  "summary": "Professional summary extracted from CV, or null if not found",
  "skills": {{
    "technical": ["Python", "JavaScript", "etc"],
    "soft": ["Leadership", "Communication", "etc"],
    "tools": ["Git", "Docker", "etc"],
    "languages": ["English", "Spanish", "etc"]
  }},
  "experience": [
    {{
      "title": "Job Title",
      "company": "Company Name",
      "dates": "Start Date - End Date",
      "description": "Key responsibilities and achievements"
    }}
  ],
  "education": [
    {{
      "degree": "Degree Name",
      "institution": "University/School Name",
      "dates": "Year or date range",
      "details": "GPA, honors, relevant coursework, or null"
    }}
  ],
  "projects": [
    {{
      "name": "Project Name",
      "description": "What the project does",
      "skills": ["skill1", "skill2"]
    }}
  ],
  "recommendations": [
    "Specific actionable suggestion 1",
    "Specific actionable suggestion 2",
    "Specific actionable suggestion 3"
  ],
  "score": 7,
  "quick_stats": {{
    "total_skills": 0,
    "total_projects": 0,
    "total_experience_entries": 0,
    "total_education_entries": 0
  }}
}}

IMPORTANT REMINDERS:
- Output ONLY the JSON object. Nothing else.
- No markdown. No code fences. No explanation text.
- All string values must be properly escaped for JSON.
- The "score" should be an integer from 1 to 10 rating the overall CV quality.
- "recommendations" should contain 3-5 specific, actionable suggestions to improve the CV.

RAW CV TEXT:
{raw_text}
"""