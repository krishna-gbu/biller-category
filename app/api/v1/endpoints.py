from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from pathlib import Path
from datetime import datetime
import os
import tempfile
import shutil

from app.core.pdf_extractor import PDFExtractor
from app.core.llm_client import LLMClient
from app.core.excel_writer import ExcelWriter
from app.prompts.enhanced_prompt import ENHANCED_PROMPT

router = APIRouter()

OUTPUT_DIR = Path("app/outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

@router.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@router.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    if file.size and file.size > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 50MB")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            shutil.copyfileobj(file.file, temp_pdf)
            temp_pdf_path = temp_pdf.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = Path(file.filename).stem
        output_filename = f"{original_name}_{timestamp}.xlsx"
        output_path = OUTPUT_DIR / output_filename
        # Core processing
        pdf_extractor = PDFExtractor({})
        llm_client = LLMClient()
        excel_writer = ExcelWriter()
        extraction_result = pdf_extractor.extract_text(temp_pdf_path)
        if not extraction_result['success']:
            raise HTTPException(status_code=500, detail=f"PDF extraction failed: {extraction_result.get('error', 'Unknown error')}")
        pdf_text = extraction_result['text']
        transactions = llm_client.process_with_llm(pdf_text, ENHANCED_PROMPT)
        if not transactions:
            raise HTTPException(status_code=500, detail="LLM processing failed")
        # Calculate summary statistics
        total_transactions = len(transactions)
        total_amount = sum(float(t['Amount'].replace('₹', '').replace(',', '')) for t in transactions)
        avg_amount = total_amount / total_transactions if total_transactions > 0 else 0
        unique_categories = len(set(t['Category'] for t in transactions))
        unique_merchants = len(set(t['Merchant'] for t in transactions))
        
        # Get date range
        dates = [t['Date'] for t in transactions if t['Date']]
        date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"
        
        # Category breakdown
        category_stats = {}
        for t in transactions:
            category = t['Category']
            amount = float(t['Amount'].replace('₹', '').replace(',', ''))
            if category not in category_stats:
                category_stats[category] = {'count': 0, 'total': 0}
            category_stats[category]['count'] += 1
            category_stats[category]['total'] += amount
        
        # Sort categories by total amount
        sorted_categories = sorted(category_stats.items(), key=lambda x: x[1]['total'], reverse=True)
        
        # Generate Excel file and return it directly
        excel_writer.save_to_excel(transactions, str(output_path))
        os.unlink(temp_pdf_path)
        
        # Return the Excel file directly
        return FileResponse(
            path=str(output_path),
            filename=output_filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")



 