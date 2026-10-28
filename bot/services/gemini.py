"""Gemini AI integration for voice speech-to-text and intent entity extraction."""
import json
import logging
import warnings
from typing import Any, Dict

warnings.filterwarnings("ignore", category=FutureWarning)
import google.generativeai as genai
from bot.config import settings
from bot.utils.parser import fallback_parse_text

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Siz "Hisobchi" shaxsiy moliya va vazifalar boti uchun matn/ovozni tahlil qiluvchi sun'iy intellektsiz.
Foydalanuvchi o'zbekcha (lotin/kirill) yoki ruscha matn yoki audio yuboradi.

Vazifangiz - xabardan quyidagi 3 toifadan birini aniqlash va JSON formatda qaytarish:
1. "expense" (harajat)
2. "debt" (qarz: berilgan yoki olingan)
3. "reminder" (eslatma yoki uchrashuv)
4. "unknown" (agar hech qaysi mos kelmasa)

Qaytariladigan JSON strukturasi:
{
  "type": "expense" | "debt" | "reminder" | "unknown",
  "data": {
    // Agar "expense" bo'lsa:
    "amount": float,
    "category": "oziq-ovqat" | "transport" | "kafe" | "kommunal" | "aloqa" | "salomatlik" | "kiyim" | "boshqa",
    "description": "harajat haqida qisqacha izoh"

    // Agar "debt" bo'lsa:
    "person_name": "inson ismi",
    "amount": float,
    "debt_type": "given" (qarz berdim) | "taken" (qarz oldim),
    "due_date": "YYYY-MM-DD" (agar muddat aytilgan bo'lsa, aks holda null),
    "description": "izoh"

    // Agar "reminder" bo'lsa:
    "title": "eslatma sarlavhasi",
    "remind_at": "YYYY-MM-DD HH:MM:SS" (taxminiy yoki aniq sana/vaqt, aks holda null),
    "reminder_type": "meeting" | "debt" | "general"
  },
  "raw_text": "transkripsiya qilingan asl matn"
}

Faqat va faqat toza JSON formatida javob bering, markdown ```json yoki ortiqcha so'z qo'shmang!
"""

class GeminiService:
    def __init__(self) -> None:
        self.api_key = settings.GEMINI_API_KEY.strip() if settings.GEMINI_API_KEY else ""
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_PROMPT,
                generation_config={"response_mime_type": "application/json"}
            )
        else:
            self.model = None

    async def process_text(self, text: str) -> Dict[str, Any]:
        """Process text using Gemini or fallback parser."""
        if not self.model:
            return fallback_parse_text(text)
        
        try:
            response = await self.model.generate_content_async(text)
            content = response.text.strip()
            # Clean possible markdown wrapping if any
            if content.startswith("```"):
                content = content.strip("`")
                if content.startswith("json"):
                    content = content[4:].strip()
            parsed = json.loads(content)
            if "raw_text" not in parsed:
                parsed["raw_text"] = text
            return parsed
        except Exception as e:
            logger.error(f"Gemini text processing failed: {e}")
            return fallback_parse_text(text)

    async def process_audio(self, audio_data: bytes, mime_type: str = "audio/ogg") -> Dict[str, Any]:
        """Process voice message bytes directly with Gemini Flash."""
        if not self.model:
            return {
                "type": "unknown",
                "data": {},
                "raw_text": "Gemini API kaliti o'rnatilmaganligi sababli ovozli xabarni tahlil qilib bo'lmadi."
            }

        try:
            audio_part = {
                "mime_type": mime_type,
                "data": audio_data
            }
            prompt = "Ushbu ovozli xabarni transkripsiya qiling va tahlil qilib kerakli JSON shakliga keltiring."
            response = await self.model.generate_content_async([prompt, audio_part])
            content = response.text.strip()
            if content.startswith("```"):
                content = content.strip("`")
                if content.startswith("json"):
                    content = content[4:].strip()
            parsed = json.loads(content)
            return parsed
        except Exception as e:
            logger.error(f"Gemini audio processing failed: {e}")
            return {
                "type": "unknown",
                "data": {},
                "raw_text": f"Ovozni qayta ishlashda xatolik yuz berdi: {str(e)}"
            }

gemini_service = GeminiService()
