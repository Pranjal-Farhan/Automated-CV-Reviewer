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
information into a clean format.

RULES:
1. Extract ONLY what you can find. Do NOT invent data.
2. If something is not found, write "Not Found".
3. For PROJECTS: Project Name: [Skill1, Skill2, Skill3](if mentioned)
4. If no projects exist, write "No Projects Found".
5. Be smart about multi-column text — reconstruct the meaning.

OUTPUT FORMAT:

──────────────────────────────────────
📌 CANDIDATE INFORMATION
──────────────────────────────────────
Full Name       : <name>
Phone Number    : <phone>
Email           : <email>
Location        : <city/country>
Website/LinkedIn: <url or Not Found>

──────────────────────────────────────
📝 SUMMARY
──────────────────────────────────────
<professional summary if found>

──────────────────────────────────────
🎓 EDUCATION
──────────────────────────────────────
- <degree> | <institution> | <year>

──────────────────────────────────────
🛠️ ALL SKILLS FOUND
──────────────────────────────────────
<every skill mentioned anywhere in the CV>

──────────────────────────────────────
💼 EXPERIENCE
──────────────────────────────────────
- <role> at <company> (<duration>)
  Responsibilities: <details>

──────────────────────────────────────
🚀 PROJECTS & PROJECT-SPECIFIC SKILLS
──────────────────────────────────────
- <project>: [skill1, skill2, skill3]

──────────────────────────────────────
📊 QUICK STATS
──────────────────────────────────────
Total Skills Found       : <count>
Total Projects Found     : <count>
Total Experience Entries  : <count>
──────────────────────────────────────

RAW CV TEXT:
{raw_text}
"""