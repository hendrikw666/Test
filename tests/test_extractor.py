"""Tests for PDF extractor module."""
import pytest
from pathlib import Path
from app.extractor import PDFExtractor
from app.models import ExtractionResult


@pytest.fixture
def extractor():
    """Create extractor instance."""
    return PDFExtractor(extract_text=True, extract_tables=True)


def test_extractor_initialization():
    """Test extractor initialization."""
    extractor = PDFExtractor()
    assert extractor.extract_text is True
    assert extractor.extract_tables is True


def test_extract_nonexistent_file(extractor):
    """Test extraction with non-existent file."""
    result = extractor.extract("/path/to/nonexistent/file.pdf")
    assert result.success is False
    assert result.error is not None
    assert "File not found" in result.error


def test_extract_invalid_extension(extractor, tmp_path):
    """Test extraction with invalid file extension."""
    # Create a non-PDF file
    invalid_file = tmp_path / "test.txt"
    invalid_file.write_text("This is not a PDF")
    
    result = extractor.extract(str(invalid_file))
    assert result.success is False
    assert result.error is not None
