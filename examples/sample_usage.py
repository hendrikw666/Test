"""Example usage of PDF extractor."""
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.extractor import PDFExtractor
from app.utils import format_table_for_csv


def main():
    """Example extraction and CSV conversion."""
    if len(sys.argv) < 2:
        print("Usage: python sample_usage.py <pdf_file>")
        print("Example: python sample_usage.py document.pdf")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    # Initialize extractor
    extractor = PDFExtractor(extract_text=True, extract_tables=True)
    
    # Extract content
    print(f"Extracting content from: {pdf_file}")
    result = extractor.extract(pdf_file)
    
    if not result.success:
        print(f"Error: {result.error}")
        sys.exit(1)
    
    print(f"\n✓ Successfully extracted {result.total_pages} pages\n")
    
    # Process each page
    for page in result.pages:
        print(f"\n{'='*60}")
        print(f"PAGE {page.page_number}")
        print(f"{'='*60}")
        
        # Print text
        if page.text:
            print("\n--- TEXT CONTENT ---")
            print(page.text[:500])  # Print first 500 chars
            if len(page.text) > 500:
                print("... [truncated]")
        
        # Print tables
        if page.tables:
            print(f"\n--- TABLES ({len(page.tables)} found) ---")
            for table in page.tables:
                print(f"\nTable {table.table_number}:")
                # Show as text format
                csv_format = format_table_for_csv(table.rows)
                print(csv_format)
    
    # Save to JSON for further processing
    output_file = f"{Path(pdf_file).stem}_extracted.json"
    with open(output_file, "w") as f:
        json.dump(result.model_dump(), f, indent=2)
    print(f"\n✓ Full results saved to: {output_file}")


if __name__ == "__main__":
    main()
