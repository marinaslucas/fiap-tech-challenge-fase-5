import json
import re
from typing import Any

from app.config import settings


class LlmService:
    ALLOWED_MODELS = {"gemini-3.1-flash-lite", "gemini-3.5-flash"}

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or settings.gemini_api_key
        self.model = self._safe_model(model or settings.gemini_model)
        self.last_error: str | None = None

    def is_enabled(self) -> bool:
        return bool(settings.llm_enabled and self.api_key)

    def generate_json(self, prompt: str) -> dict[str, Any] | None:
        self.last_error = None
        text = self.generate_text(prompt)
        if not text:
            return None

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, flags=re.DOTALL)
            if not match:
                self.last_error = "Gemini response was not valid JSON."
                return None

        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            self.last_error = "Gemini response contained malformed JSON."
            return None

    def generate_text(self, prompt: str) -> str | None:
        if not self.is_enabled():
            self.last_error = "Gemini is not configured or LLM usage is disabled."
            return None

        try:
            from google import genai
        except ImportError:
            self.last_error = "google-genai is not installed."
            return None

        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return response.text
        except Exception as error:
            self.last_error = f"Gemini request failed: {error.__class__.__name__}."
            return None

    def _safe_model(self, model: str) -> str:
        if model in self.ALLOWED_MODELS:
            return model
        return "gemini-3.1-flash-lite"
