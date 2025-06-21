from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
import os
import shutil
from ocr.ocr_engine import extract_text_from_image, extract_text_from_pdf
from llm_agent.llm_interface import classify_invoice
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from sheets_integration import initialize_sheets_client, append_invoice_to_llc_tab

SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "SortAI Invoices")

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
async def upload_invoices(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload multiple invoice files (PDF or image) and classify them using an LLM.
    Results are automatically logged to Google Sheets organized by LLC.
    """
    results = []
    
    # Initialize Google Sheets client once for all uploads
    try:
        sheets_client = initialize_sheets_client()
        spreadsheet = sheets_client.open(SPREADSHEET_NAME)
        sheets_enabled = True
    except Exception as e:
        print(f"⚠️ Google Sheets initialization failed: {str(e)}")
        sheets_enabled = False

    for file in files:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            # OCR processing
            if file.filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(temp_path)
            else:
                text = extract_text_from_image(temp_path)

            # LLM classification
            result = classify_invoice(text, llc_metadata)
            print(f"✅ Processed {file.filename}: {result}")
            
            # Prepare data for Google Sheets
            if sheets_enabled and result.get("llc_name"):
                invoice_data = {
                    "filename": file.filename,
                    "vendor": result.get("invoice_summary", {}).get("vendor", ""),
                    "amount": result.get("invoice_summary", {}).get("amount", ""),
                    "date": result.get("invoice_summary", {}).get("date", ""),
                    "address": result.get("invoice_summary", {}).get("address", ""),
                    "order_number": result.get("invoice_summary", {}).get("order_number", ""),
                    "invoice_number": result.get("invoice_summary", {}).get("invoice_number", ""),
                    "reasoning": result.get("reasoning", "")
                }
                
                try:
                    append_invoice_to_llc_tab(spreadsheet, result["llc_name"], invoice_data)
                except Exception as sheets_error:
                    print(f"⚠️ Failed to log to sheets: {str(sheets_error)}")
            
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
