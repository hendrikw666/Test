"""PDF extraction logic using pdfplumber."""
import pdfplumber
from typing import List, Optional
from app.models import ExtractionResult, PageContent, ExtractedTable
from app.utils import clean_text, validate_file


class PDFExtractor:
    """Handles PDF extraction operations."""
    
    def __init__(self, extract_text: bool = True, extract_tables: bool = True):
        """Initialize extractor.
        
        Args:
            extract_text: Whether to extract text content
            extract_tables: Whether to extract tables
        """
        self.extract_text = extract_text
        self.extract_tables = extract_tables
    
    def extract(self, filepath: str) -> ExtractionResult:
        """Extract content from PDF file.
        
        Args:
            filepath: Path to PDF file
            
        Returns:
            ExtractionResult with extracted content
        """
        # Validate file
        is_valid, error = validate_file(filepath)
        if not is_valid:
            return ExtractionResult(
                filename=filepath,
                success=False,
                total_pages=0,
                pages=[],
                error=error
            )
        
        try:
            with pdfplumber.open(filepath) as pdf:
                total_pages = len(pdf.pages)
                pages_content = []
                
                for page_idx, page in enumerate(pdf.pages, 1):
                    page_data = self._extract_page_content(page, page_idx)
                    pages_content.append(page_data)
                
                return ExtractionResult(
                    filename=filepath,
                    success=True,
                    total_pages=total_pages,
                    pages=pages_content,
                    error=None
                )
        
        except Exception as e:
            return ExtractionResult(
                filename=filepath,
                success=False,
                total_pages=0,
                pages=[],
                error=f"Extraction failed: {str(e)}"
            )
    
    def _extract_page_content(self, page, page_number: int) -> PageContent:
        """Extract content from a single page.
        
        Args:
            page: pdfplumber page object
            page_number: Page number (1-indexed)
            
        Returns:
            PageContent object
        """
        text = ""
        tables = []
        
        # Extract text
        if self.extract_text:
            raw_text = page.extract_text() or ""
            text = clean_text(raw_text)
        
        # Extract tables
        if self.extract_tables:
            page_tables = page.extract_tables() or []
            for table_idx, table_data in enumerate(page_tables, 1):
                extracted_table = ExtractedTable(
                    table_number=table_idx,
                    rows=table_data,
                    page=page_number
                )
                tables.append(extracted_table)
        
        return PageContent(
            page_number=page_number,
            text=text,
            tables=tables
        )
    
    def extract_batch(self, filepaths: List[str]) -> tuple[List[ExtractionResult], List[str]]:
        """Extract content from multiple PDF files.
        
        Args:
            filepaths: List of file paths
            
        Returns:
            Tuple of (successful_results, failed_filepaths)
        """
        results = []
        failed = []
        
        for filepath in filepaths:
            result = self.extract(filepath)
            if result.success:
                results.append(result)
            else:
                failed.append(filepath)
        
        return results, failed
