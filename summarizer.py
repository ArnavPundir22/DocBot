import google.generativeai as genai
from config import GEMINI_API_KEY
from PIL import Image
from utils import chunk_text

genai.configure(api_key=GEMINI_API_KEY)

text_model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
vision_model = genai.GenerativeModel("models/gemini-1.5-pro-latest")  # ✅ Fixed

def summarize_text(text: str) -> str:
    try:
        chunks = chunk_text(text)
        summaries = []
        for chunk in chunks:
            response = text_model.generate_content(f"Summarize this chunk clearly:\n{chunk}")
            summaries.append(response.text)
        return "\n".join(summaries)
    except Exception as e:
        return f"[Error]: {str(e)}"

def summarize_images(image_paths: list) -> str:
    try:
        captions = []
        for path in image_paths:
            image = Image.open(path)
            response = vision_model.generate_content(["Summarize the content of this image:", image])
            captions.append(response.text)
        return "\n\n".join(captions)
    except Exception as e:
        return f"[Vision Error]: {str(e)}"
