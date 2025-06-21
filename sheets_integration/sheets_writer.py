"""
sheets_writer.py
Google Sheets integration for Sort.ai invoice logging system.
"""

import gspread
from google.oauth2.service_account import Credentials
from typing import Dict, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define the scope for Google Sheets API
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Column headers for each LLC tab
INVOICE_HEADERS = [
    "filename", 
    "vendor", 
    "amount", 
    "date", 
    "address", 
    "order_number", 
    "invoice_number", 
    "reasoning"
]


def initialize_sheets_client() -> gspread.Client:
    """
    Authenticate and return a Google Sheets client using service account credentials.
    
    Expects GOOGLE_SERVICE_ACCOUNT_PATH environment variable pointing to JSON key file.
    
    :return: Authenticated gspread client
    :rtype: gspread.Client
    :raises: FileNotFoundError if service account file not found
    :raises: Exception if authentication fails
    """
    try:
        # Get service account path from environment
        service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        if not service_account_path:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        
        if not os.path.exists(service_account_path):
            raise FileNotFoundError(f"Service account file not found: {service_account_path}")
        
        # Load credentials and authorize client
        credentials = Credentials.from_service_account_file(
            service_account_path, 
            scopes=SCOPES
        )
        
        client = gspread.authorize(credentials)
        return client
        
    except Exception as e:
        print(f"❌ Failed to initialize Google Sheets client: {str(e)}")
        raise


def open_or_create_llc_tab(sheet: gspread.Spreadsheet, llc_name: str) -> gspread.Worksheet:
    """
    Open an existing tab for the LLC or create one if it doesn't exist.
    
    :param sheet: The main spreadsheet object
    :type sheet: gspread.Spreadsheet
    :param llc_name: Name of the LLC (will be used as tab name)
    :type llc_name: str
    :return: The worksheet for the specified LLC
    :rtype: gspread.Worksheet
    """
    try:
        # Try to open existing worksheet
        worksheet = sheet.worksheet(llc_name)
        print(f"✅ Found existing tab: {llc_name}")
        return worksheet
        
    except gspread.WorksheetNotFound:
        # Create new worksheet if it doesn't exist
        print(f"📝 Creating new tab: {llc_name}")
        
        try:
            # Add new worksheet
            worksheet = sheet.add_worksheet(title=llc_name, rows=1000, cols=len(INVOICE_HEADERS))
            
            # Add headers to the first row
            worksheet.append_row(INVOICE_HEADERS)
            
            # Format headers (bold)
            worksheet.format('A1:H1', {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}
            })
            
            print(f"✅ Created new tab with headers: {llc_name}")
            return worksheet
            
        except Exception as e:
            print(f"❌ Failed to create tab {llc_name}: {str(e)}")
            raise


def append_invoice_to_llc_tab(sheet: gspread.Spreadsheet, llc_name: str, invoice_data: Dict) -> None:
    """
    Append invoice data to the appropriate LLC worksheet in the spreadsheet.
    
    :param sheet: The main spreadsheet object
    :type sheet: gspread.Spreadsheet
    :param llc_name: Name of the LLC (determines which tab to write to)
    :type llc_name: str
    :param invoice_data: Dictionary containing invoice fields
    :type invoice_data: Dict
    
    Expected invoice_data format:
    {
        "filename": "invoice123.pdf",
        "vendor": "Amazon", 
        "amount": "$299.99",
        "date": "2025-06-20",
        "address": "123 Elm St",
        "order_number": "ORD-7882",
        "invoice_number": "INV-2231", 
        "reasoning": "Matched Amazon and 123 Elm St to Ocean View LLC"
    }
    """
    try:
        # Get or create the worksheet for this LLC
        worksheet = open_or_create_llc_tab(sheet, llc_name)
        
        # Extract values in the order of headers
        row_data = [
            invoice_data.get("filename", ""),
            invoice_data.get("vendor", ""),
            invoice_data.get("amount", ""), 
            invoice_data.get("date", ""),
            invoice_data.get("address", ""),
            invoice_data.get("order_number", ""),
            invoice_data.get("invoice_number", ""),
            invoice_data.get("reasoning", "")
        ]
        
        # Append the row to the worksheet
        worksheet.append_row(row_data)
        
        print(f"✅ Successfully logged invoice to {llc_name}: {invoice_data.get('filename', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Failed to append invoice to {llc_name}: {str(e)}")
        raise


def test_sheets_connection() -> bool:
    """
    Test function to verify Google Sheets connection and permissions.
    
    :return: True if connection successful, False otherwise
    :rtype: bool
    """
    try:
        client = initialize_sheets_client()
        
        # Try to list spreadsheets (basic permission test)
        spreadsheets = client.list_permissions()
        print("✅ Google Sheets connection test successful")
        return True
        
    except Exception as e:
        print(f"❌ Google Sheets connection test failed: {str(e)}")
        return False