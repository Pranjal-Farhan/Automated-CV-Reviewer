import os
import json
from dotenv import load_dotenv
from google import genai

from .base_analyzer import BaseAnalyzer
from ..prompts.prompt_builder import PromptBuilder


class GeminiAnalyzer(BaseAnalyzer):

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError(
                "❌ GOOGLE_API_KEY not found!\n"
                "   Create analyzer/.env with: GOOGLE_API_KEY=your_key"
            )

        self._client = genai.Client(api_key=api_key)
        self._model_name = "gemini-2.5-flash"

        print(f"✅ GeminiAnalyzer initialized: {self._model_name}")

    def get_model_name(self) -> str:
        return self._model_name

    def analyze_raw_text(self, raw_text: str) -> str:       
        prompt = PromptBuilder.build_raw_text_prompt(raw_text)

        try:
            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,
                config={
                    "temperature": 0.1,
                    "max_output_tokens": 10000,
                }
            )
            return response.text

        except Exception as e:
            return f"❌ Gemini API Error: {e}"
