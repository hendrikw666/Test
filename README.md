# PDF Extraction Service

A FastAPI-based service for extracting text and tables from PDF documents. Designed to prepare data for CSV conversion and downstream processing.

## Features

- ✅ Extract text content from all pages
- ✅ Automatically detect and extract tables
- ✅ REST API for single and batch processing
- ✅ Handle up to 100 files per batch
- ✅ Clean, structured JSON output
- ✅ Docker support for easy deployment
- ✅ Comprehensive API documentation
- ✅ Unit tests included

## Quick Start

### Option 1: Local Development

```bash
# Clone and setup
git clone <repo-url>
cd Test

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Option 2: Docker

```bash
# Build and run
docker-compose up

# The service will be available at http://localhost:8000
```

### Option 3: Command Line

```bash
# Extract from a single PDF
python examples/sample_usage.py path/to/document.pdf

# Output saved to: document_extracted.json
```

## API Endpoints

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Single File Extraction

```bash
POST /api/extract
```

**Request:**
```bash
curl -X POST "http://localhost:8000/api/extract" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "filename": "document.pdf",
  "success": true,
  "total_pages": 3,
  "pages": [
    {
      "page_number": 1,
      "text": "Extracted text content...",
      "tables": [
        {
          "table_number": 1,
          "rows": [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
          ],
          "page": 1
        }
      ]
    }
  ]
}
```

### Batch Extraction

```bash
POST /api/extract-batch
```

**Request:**
```bash
curl -X POST "http://localhost:8000/api/extract-batch" \
  -F "files=@document1.pdf" \
  -F "files=@document2.pdf" \
  -F "files=@document3.pdf"
```

**Response:**
```json
{
  "total_files": 3,
  "successful": 3,
  "failed": 0,
  "results": [
    { "...extraction result..." }
  ]
}
```

## Configuration

Edit `config.py` to customize:

```python
MAX_FILE_SIZE = 50 * 1024 * 1024  # Maximum file size: 50MB
MAX_BATCH_SIZE = 100               # Maximum files per batch
EXTRACT_TEXT = True                # Extract text content
EXTRACT_TABLES = True              # Extract tables
```

## Output Format

Extracted data is returned in structured JSON with three main components:

1. **Text Content**: Raw extracted text from each page
2. **Tables**: 2D array format, ready for CSV conversion
3. **Metadata**: Page numbers, success status, error messages

### Converting Tables to CSV

Use the extracted table data to generate CSV files:

```python
from app.utils import format_table_for_csv

# From extraction result
for page in result.pages:
    for table in page.tables:
        csv_content = format_table_for_csv(table.rows)
        with open(f'table_{table.table_number}.csv', 'w') as f:
            f.write(csv_content)
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app

# Run specific test
pytest tests/test_extractor.py -v
```

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── extractor.py         # PDF extraction logic
│   ├── models.py            # Pydantic models
│   └── utils.py             # Utility functions
├── tests/
│   ├── test_api.py
│   ├── test_extractor.py
│   └── test_utils.py
├── examples/
│   └── sample_usage.py      # CLI example
├── config.py                # Configuration
├── requirements.txt         # Dependencies
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Performance Considerations

- **Single File**: ~100-500ms per page (varies by PDF complexity)
- **Batch Processing**: Process multiple files sequentially; adjust `MAX_BATCH_SIZE` based on available memory
- **File Size Limit**: Set to 50MB by default; increase in `config.py` if needed
- **OCR**: Not enabled by default; add Tesseract support if scanned PDFs needed

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **pdfplumber**: PDF content extraction
- **Pydantic**: Data validation
- **pytest**: Testing framework

## Future Enhancements

- [ ] OCR support for scanned PDFs
- [ ] Webhook callbacks for batch processing
- [ ] Database storage for extraction results
- [ ] Async batch processing
- [ ] Image extraction
- [ ] Metrics and monitoring
- [ ] Authentication & API keys

## Troubleshooting

### "ModuleNotFoundError: No module named 'pdfplumber'"

```bash
pip install -r requirements.txt
```

### "Port 8000 already in use"

```bash
# Use a different port
python -m uvicorn app.main:app --port 8001
```

### "Permission denied" on uploads

Ensure the `uploads/` directory has write permissions:

```bash
chmod -R 755 uploads/
```

## License

MIT License - feel free to use this in your projects!

## Support

For issues or questions:
1. Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
2. Review [pdfplumber documentation](https://github.com/jsvine/pdfplumber)
3. Open an issue on GitHub
