"""FastAPI application for PDF extraction service."""
from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

import config
from app.extractor import PDFExtractor
from app.models import ExtractionResult, BatchExtractionResult, HealthResponse

# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version=config.APP_VERSION,
    description="Extract text and tables from PDF documents"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PDF extractor
extractor = PDFExtractor(
    extract_text=config.EXTRACT_TEXT,
    extract_tables=config.EXTRACT_TABLES
)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=config.APP_VERSION
    )


@app.post("/api/extract", response_model=ExtractionResult, tags=["Extraction"])
async def extract_pdf(file: UploadFile = File(...)):
    """Extract text and tables from a single PDF file.
    
    Args:
        file: PDF file to extract from
        
    Returns:
        ExtractionResult with extracted content
    """
    # Validate file extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    # Save uploaded file temporarily
    temp_path = config.UPLOAD_DIR / file.filename
    try:
        contents = await file.read()
        with open(temp_path, "wb") as f:
            f.write(contents)
        
        # Extract content
        result = extractor.extract(str(temp_path))
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if temp_path.exists():
            os.remove(temp_path)


@app.post("/api/extract-batch", response_model=BatchExtractionResult, tags=["Extraction"])
async def extract_batch(files: List[UploadFile] = File(...)):
    """Extract text and tables from multiple PDF files.
    
    Args:
        files: List of PDF files to extract from
        
    Returns:
        BatchExtractionResult with results for all files
    """
    if len(files) > config.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum batch size is {config.MAX_BATCH_SIZE}"
        )
    
    # Validate all files
    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file: {file.filename}. Only PDF files are supported"
            )
    
    results = []
    failed_count = 0
    temp_paths = []
    
    try:
        # Save all files temporarily
        for file in files:
            temp_path = config.UPLOAD_DIR / file.filename
            contents = await file.read()
            with open(temp_path, "wb") as f:
                f.write(contents)
            temp_paths.append(temp_path)
        
        # Extract content from all files
        for temp_path in temp_paths:
            result = extractor.extract(str(temp_path))
            results.append(result)
            if not result.success:
                failed_count += 1
        
        return BatchExtractionResult(
            total_files=len(files),
            successful=len(results) - failed_count,
            failed=failed_count,
            results=results
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing batch: {str(e)}"
        )
    
    finally:
        # Clean up all temporary files
        for temp_path in temp_paths:
            if temp_path.exists():
                os.remove(temp_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
