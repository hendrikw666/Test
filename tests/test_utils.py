"""Tests for utility functions."""
import pytest
from app.utils import clean_text, format_table_for_csv, extract_text_from_table


def test_clean_text():
    """Test text cleaning."""
    dirty_text = """  Line 1  

    Line 2  
  Line 3  """
    
    cleaned = clean_text(dirty_text)
    assert "Line 1" in cleaned
    assert "Line 2" in cleaned
    assert "Line 3" in cleaned
    # No excessive whitespace
    assert "  " not in cleaned


def test_format_table_for_csv():
    """Test table to CSV formatting."""
    table = [
        ["Name", "Age"],
        ["John", "30"],
        ["Jane", "25"]
    ]
    
    csv = format_table_for_csv(table)
    lines = csv.split('\n')
    assert len(lines) == 3
    assert "Name" in lines[0]


def test_extract_text_from_table():
    """Test table to text conversion."""
    table = [
        ["Name", "Age"],
        ["John", "30"],
        ["Jane", "25"]
    ]
    
    text = extract_text_from_table(table)
    assert "Name" in text
    assert "John" in text
    assert "Jane" in text
