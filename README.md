# Sort.ai 🧾🤖

**Sort.ai** is an AI-powered invoice classification tool built for property management teams. It uses OCR and a Large Language Model (LLM) to intelligently extract and classify invoices to the correct LLC based on address metadata.

## 🔍 Features

- 📤 Upload **multiple invoice files** at once (PDF or image)
- 🧠 Uses an LLM (e.g., GPT-4) to reason about invoice content
- 📌 Classifies invoices by matching addresses with known LLCs
- 📄 Supports **OCR** with Tesseract for text extraction
- 🌐 Web-based UI for uploading files via HTML form
- 🦺 Graceful error handling and clean logs
- 🛠️ Built with FastAPI and Python

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/sortai.git
cd sortai
```

### 2. Create a virtual environment

```bash
python -m venv venv
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-key-here
```

> You’ll need an OpenAI API key with GPT-4 access.

### 5. Install Tesseract

Make sure [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) is installed and added to your system PATH.

- On macOS: `brew install tesseract`
- On Ubuntu: `sudo apt install tesseract-ocr`
- On Windows: [Download the installer](https://github.com/UB-Mannheim/tesseract/wiki) and add it to your PATH

## 💡 Usage

### Start the server:

```bash
uvicorn main:app --reload
```

### Open the app:

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.  
Upload one or more invoices (PDF or image), and the LLM will return structured classification results for each file.

## 📂 Project Structure

```
sortai/
├── main.py                  # FastAPI backend + routes
├── upload.html              # Simple HTML upload form
├── .env                     # API keys (not tracked in git)
├── requirements.txt         # All dependencies
├── ocr/
│   └── ocr_engine.py        # PDF/image OCR processing
├── llm_agent/
│   └── llm_interface.py     # Handles GPT classification
```

## 🧠 LLM Logic

The LLM is prompted with:

- The OCR-extracted text from each invoice
- A dictionary of known LLCs and their associated addresses

It responds with:

- The most likely LLC the invoice belongs to
- A structured invoice summary (vendor, amount, date, address)
- Reasoning for the classification

Example output:

```json
{
  "llc_name": "Main Street Holdings LLC",
  "invoice_summary": {
    "vendor": "CleanPro Janitorial Services",
    "amount": "$375.00",
    "date": "2025-06-15",
    "address": "120 Main St Boston MA 02110"
  },
  "reasoning": "The service address matches one of the addresses registered under Main Street Holdings LLC."
}
```

## 🛣️ Roadmap

- [ ] Add database support to store LLC metadata and invoice history
- [ ] Create an admin dashboard for reviewing classification history
- [ ] Allow users to upload LLC metadata via UI
- [ ] Add user authentication
- [ ] Deploy the app (Render, Railway, EC2, etc.)
- [ ] Add Stripe billing for usage-based pricing

## 🤝 Contributing

Pull requests are welcome! If you’d like to fork, extend, or integrate this into your own company’s workflow, feel free to get in touch.

## 🧑‍💼 License

MIT License

---

> Built with 💡 by Eitam Shapsa – helping property managers automate and scale their back-office workflows.