"""Pydantic models for request/response validation."""
from typing import List, Optional, Any
from pydantic import BaseModel, Field


class ExtractedTable(BaseModel):
    """Extracted table data."""
    table_number: int = Field(..., description="Sequential table number")
    rows: List[List[Optional[str]]] = Field(..., description="Table data as 2D array")
    page: int = Field(..., description="Page number where table was found")


class PageContent(BaseModel):
    """Extracted content from a single page."""
    page_number: int = Field(..., description="Page number (1-indexed)")
    text: str = Field(..., description="Extracted text content")
    tables: List[ExtractedTable] = Field(default_factory=list, description="Tables found on page")


class ExtractionResult(BaseModel):
    """Result of PDF extraction."""
    filename: str = Field(..., description="Original filename")
    success: bool = Field(..., description="Whether extraction was successful")
    total_pages: int = Field(..., description="Total number of pages")
    pages: List[PageContent] = Field(..., description="Content from each page")
    error: Optional[str] = Field(None, description="Error message if extraction failed")


class BatchExtractionResult(BaseModel):
    """Result of batch extraction."""
    total_files: int = Field(..., description="Total files processed")
    successful: int = Field(..., description="Successfully extracted files")
    failed: int = Field(..., description="Failed extractions")
    results: List[ExtractionResult] = Field(..., description="Results for each file")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Service version")
