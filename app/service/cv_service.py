import os
import uuid
import asyncio
import tempfile
from pathlib import Path

from app.service.parser.factory.parser_factory import ParserFactory
from app.service.analyzer.analyzers.gemini_analyzer import GeminiAnalyzer

from app.repository.cv_repository import CVRepository
from app.models.schemas import JobStatus


class CVService:

    @staticmethod
    def generate_job_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    async def create_job(filename: str) -> str:
        job_id = CVService.generate_job_id()
        await CVRepository.create_job(job_id, filename)
        return job_id

    @staticmethod
    async def process_cv(job_id: str, file_content: bytes, filename: str):
        try:
            await CVRepository.update_status(job_id, JobStatus.PROCESSING)

            raw_text, analysis_result = await asyncio.to_thread(
                CVService._parse_and_analyze, file_content, filename
            )

            if raw_text is None:
                await CVRepository.save_error(job_id, "Parser returned empty text.")
                return

            if analysis_result.startswith("❌"):
                await CVRepository.save_error(job_id, analysis_result)
                return

            await CVRepository.save_result(job_id, raw_text, analysis_result)

        except Exception as e:
            await CVRepository.save_error(job_id, f"Processing error: {str(e)}")

    @staticmethod
    def _parse_and_analyze(file_content: bytes, filename: str) -> tuple:
        suffix = Path(filename).suffix.lower()

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            if suffix == ".pdf":
                parser = ParserFactory.create("pdfplumber")
                raw_text = parser.extract_text(Path(tmp_path))
            elif suffix == ".txt":
                raw_text = file_content.decode("utf-8")
            else:
                return None, None

            if not raw_text or not raw_text.strip():
                return None, None

            analyzer = GeminiAnalyzer()
            analysis_result = analyzer.analyze_raw_text(raw_text)

            return raw_text, analysis_result

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    @staticmethod
    async def get_result(job_id: str) -> dict | None:
        return await CVRepository.get_job_by_id(job_id)