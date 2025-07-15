# pdf_handler.py

import fitz  # PyMuPDF
from PIL import Image
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text

def extract_images_from_pdf(pdf_path, output_folder="pdf_images"):
    doc = fitz.open(pdf_path)
    image_paths = []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for page_index in range(len(doc)):
        images = doc.get_page_images(page_index)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = os.path.join(output_folder, f"page{page_index+1}_{img_index}.{image_ext}")

            with open(image_path, "wb") as f:
                f.write(image_bytes)
            image_paths.append(image_path)

    doc.close()
    return image_paths
