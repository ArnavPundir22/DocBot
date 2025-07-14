# qa_engine.py
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")


def answer_question(context: str, question: str) -> str:
    try:
        prompt = f"""Based on the following documentation:\n\n{context}\n\nAnswer the question:\n{question}"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[Error]: {str(e)}"
