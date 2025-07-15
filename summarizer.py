# summarizer.py
import os
from key_manager import GeminiKeyManager
import google.generativeai as genai

key_manager = GeminiKeyManager()
text_model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
vision_model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

def summarize_text(text: str) -> str:
    try:
        response = text_model.generate_content(f"Summarize this documentation clearly:\n{text}")
        return response.text
    except Exception as e:
        if "429" in str(e):
            try:
                key_manager.rotate_key()
                return summarize_text(text)  # Retry
            except RuntimeError as ex:
                return f"[Quota Error]: {str(ex)}"
        return f"[Error]: {str(e)}"

def summarize_images(image_paths: list) -> str:
    if not image_paths:
        return "No images found in PDF."

    summaries = []
    for path in image_paths:
        try:
            with open(path, "rb") as img_file:
                response = vision_model.generate_content(
                    [f"Summarize the content of this image briefly:", img_file],
                    stream=False
                )
                summaries.append(f"{os.path.basename(path)}: {response.text}")
        except Exception as e:
            if "429" in str(e):
                try:
                    key_manager.rotate_key()
                    return summarize_images(image_paths)  # Retry
                except RuntimeError as ex:
                    return f"[Quota Error]: {str(ex)}"
            summaries.append(f"{os.path.basename(path)}: [Vision Error]: {str(e)}")
    return "\n".join(summaries)
