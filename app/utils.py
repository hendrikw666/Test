"""Utility functions for PDF extraction."""
import os
from pathlib import Path
from typing import Optional
from config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE


def validate_file(filepath: str) -> tuple[bool, Optional[str]]:
    """Validate if file is a valid PDF.
    
    Args:
        filepath: Path to file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not Path(filepath).exists():
        return False, f"File not found: {filepath}"
    
    if not filepath.lower().endswith(".pdf"):
        return False, f"Invalid file extension. Allowed: {ALLOWED_EXTENSIONS}"
    
    file_size = os.path.getsize(filepath)
    if file_size > MAX_FILE_SIZE:
        return False, f"File size ({file_size}) exceeds maximum ({MAX_FILE_SIZE})"
    
    if file_size == 0:
        return False, "File is empty"
    
    return True, None


def clean_text(text: str) -> str:
    """Clean extracted text.
    
    Args:
        text: Raw extracted text
        
    Returns:
        Cleaned text
    """
    # Remove excessive whitespace
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    lines = [line for line in lines if line]  # Remove empty lines
    return '\n'.join(lines)


def format_table_for_csv(table: list[list]) -> str:
    """Format table data for CSV conversion.
    
    Args:
        table: 2D array representing table
        
    Returns:
        CSV formatted string
    """
    csv_lines = []
    for row in table:
        # Handle None values and convert to strings
        cells = [str(cell) if cell is not None else "" for cell in row]
        # Basic CSV escaping
        escaped_cells = [f'"{cell}"' if ',' in cell or '"' in cell else cell for cell in cells]
        csv_lines.append(','.join(escaped_cells))
    return '\n'.join(csv_lines)


def extract_text_from_table(table: list[list]) -> str:
    """Convert table to human-readable text format.
    
    Args:
        table: 2D array representing table
        
    Returns:
        Formatted text representation
    """
    if not table:
        return ""
    
    # Calculate column widths
    col_widths = []
    for col_idx in range(len(table[0])):
        max_width = max(len(str(row[col_idx] or "")) for row in table)
        col_widths.append(max_width)
    
    # Format table
    lines = []
    for row in table:
        cells = []
        for col_idx, cell in enumerate(row):
            cell_str = str(cell) if cell is not None else ""
            cells.append(cell_str.ljust(col_widths[col_idx]))
        lines.append(" | ".join(cells))
    
    return "\n".join(lines)
