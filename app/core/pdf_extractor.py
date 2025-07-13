import fitz  # PyMuPDF
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PDFExtractor:
    """
    Simple PDF text extraction
    """
    def __init__(self, config: dict = None):
        self.config = config or {}

    def extract_text(self, pdf_path: str) -> dict:
        try:
            if not Path(pdf_path).exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            if not Path(pdf_path).is_file():
                raise ValueError(f"Path is not a file: {pdf_path}")
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            text = ""
            for page_num in range(page_count):
                page = doc[page_num]
                text += page.get_text() + "\n"
            doc.close()
            return {
                'success': True,
                'text': text,
                'method': 'pymupdf',
                'pages': page_count
            }
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            try:
                if 'doc' in locals():
                    doc.close()
            except:
                pass
            return {
                'success': False,
                'error': str(e)
            } 