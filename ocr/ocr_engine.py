"""
ocr_engine.py
This module provides OCR (Optical Character Recognition) functionality using pytesseract and PIL.
"""
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file using OCR.
    :param pdf_path: The path to the PDF file.
    :type pdf_path: str
    :return: The text extracted from the PDF.
    :rtype: str
    """
    images = convert_from_path(pdf_path)
    text = ""
    for i, img in enumerate(images):
        text += pytesseract.image_to_string(img) + "\n"
    return text

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
