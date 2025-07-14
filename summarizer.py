# summarizer.py
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")


def summarize_text(text: str) -> str:
    try:
        response = model.generate_content(f"Summarize this documentation clearly:\n{text}")
        return response.text
    except Exception as e:
        return f"[Error]: {str(e)}"
