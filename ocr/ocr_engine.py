"""
ocr_engine.py
This module provides OCR (Optical Character Recognition) functionality using pytesseract and PIL.
"""
from PIL import Image
import pytesseract

def extract_text_from_image(file_path: str) -> str:
    """
    Extract text from an image file using OCR.

    :param file_path: The path to the image file.
    :type file_path: str
    :return: The text extracted from the image.
    :rtype: str
    """
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)
