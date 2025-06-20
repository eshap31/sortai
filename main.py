from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
from llm_agent.llm_interface import classify_invoice
from ocr.ocr_engine import extract_text_from_image, extract_text_from_pdf

app = FastAPI()

@app.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    """
    Endpoint to upload an invoice file (PDF or image) and classify it using LLM.
    :param file: The uploaded invoice file.
    :type file: UploadFile
    :return: The classification result from the LLM.
    :rtype: dict
    """
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # LLC data (moved here!)
        llc_metadata = {
            "Main Street Holdings LLC": ["120 Main St Boston MA 02110", "122 Main St Boston MA 02110"],
            "Grove Apartments LLC": ["44 Grove St Cambridge MA 02138"]
        }

        # Determine file type
        if file.filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(temp_path)
        else:
            text = extract_text_from_image(temp_path)

        result = classify_invoice(text, llc_metadata)
        print("🔁 GPT RESULT:", result)
        return result

    except Exception as e:
        print("❌ Error processing invoice:", str(e))
        raise HTTPException(status_code=500, detail=f"Invoice processing failed: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
