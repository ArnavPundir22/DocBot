# key_manager.py

from config import GEMINI_API_KEYS, CURRENT_KEY_INDEX
import google.generativeai as genai

class GeminiKeyManager:
    def __init__(self):
        self.keys = GEMINI_API_KEYS
        self.index = CURRENT_KEY_INDEX
        self._set_key(self.keys[self.index])

    def _set_key(self, key):
        genai.configure(api_key=key)

    def get_current_key(self):
        return self.keys[self.index]

    def rotate_key(self):
        self.index += 1
        if self.index >= len(self.keys):
            raise RuntimeError("🚫 All Gemini API keys exhausted. Please add more keys or try later.")
        self._set_key(self.keys[self.index])
        print(f"🔁 Switched to Gemini API Key #{self.index + 1}")

def is_quota_error(response: str) -> bool:
        if not response:
            return False
        return any(phrase in response.lower() for phrase in [
            "you exceeded your current quota",
            "quota limit",
            "429",
            "rate limit",
            "out of quota",
            "quota exceeded"
        ])
