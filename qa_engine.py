# qa_engine.py

import google.generativeai as genai
from key_manager import GeminiKeyManager

key_manager = GeminiKeyManager()
qa_model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

def answer_question(context: str, question: str) -> str:
    try:
        prompt = f"""Based on the following documentation:\n\n{context}\n\nAnswer the question:\n{question}"""
        response = qa_model.generate_content(prompt)
        return response.text
    except Exception as e:
        if "429" in str(e):
            try:
                key_manager.rotate_key()
                return answer_question(context, question)  # Retry
            except RuntimeError as ex:
                return f"[Quota Error]: {str(ex)}"
        return f"[Error]: {str(e)}"
