from fastapi import FastAPI, UploadFile, File
import shutil
import os
from llm_agent.llm_interface import classify_invoice
from ocr.ocr_engine import extract_text_from_image

app = FastAPI()

@app.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    """
    Handles the upload of an invoice image file, performs OCR to extract text, and classifies the invoice.
    :param file: The uploaded invoice image file.
    :type file: UploadFile
    :return: The result of the invoice classification.
    :rtype: dict
    """
    # Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # OCR
        text = extract_text_from_image(temp_path)

        # list of the known LLCs and their associated addresses
        llc_metadata = {
        "Main Street Holdings LLC": ["120 Main St Boston MA 02110", "122 Main St Boston MA 02110"],
        "Grove Apartments LLC": ["44 Grove St Cambridge MA 02138"]
}

        result = classify_invoice(text, llc_metadata)
        # Log the result for debugging
        print("🔁 GPT RESULT:", result)  # <== Add this
        return result

    finally:
        # Clean up
        os.remove(temp_path)
