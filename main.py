from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import os
import shutil
from ocr.ocr_engine import extract_text_from_image, extract_text_from_pdf
from llm_agent.llm_interface import classify_invoice
from fastapi.staticfiles import StaticFiles


app = FastAPI()

llc_metadata = {
    "Main Street Holdings LLC": ["120 Main St Boston MA 02110", "122 Main St Boston MA 02110"],
    "Grove Apartments LLC": ["44 Grove St Cambridge MA 02138"],
    "Elmhurt Holdings LLC": ["9232 50th Ave 3RD Floor, Elmhurst, NY 11373"]
}

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/upload.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload")
async def upload_invoices(
    files: List[UploadFile] = File(...)):
    """
    Endpoint to upload multiple invoice files (PDF or image) and classify them using an LLM.

    Each file is processed using OCR to extract text, and then classified into the correct LLC
    based on known metadata (e.g., addresses tied to each LLC). Results for each file are returned
    as a list of dictionaries.

    :param files: A list of uploaded invoice files (PDFs or images).
    :type files: List[UploadFile]
    :return: A list of results for each invoice, including the filename and either a classification result or an error.
    :rtype: List[dict]
    """

    results = []

    for file in files:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            if file.filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(temp_path)
            else:
                text = extract_text_from_image(temp_path)

            result = classify_invoice(text, llc_metadata)
            print(f"✅ Processed {file.filename}: {result}")
            results.append({"filename": file.filename, "result": result})

        except Exception as e:
            print(f"❌ Failed to process {file.filename}: {str(e)}")
            results.append({
                "filename": file.filename,
                "error": f"Failed to process: {str(e)}"
            })

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    return results
