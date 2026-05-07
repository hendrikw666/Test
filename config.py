"""Configuration module for PDF extraction service."""
import os
from pathlib import Path

# Application settings
APP_NAME = "PDF Extraction Service"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False") == "True"

# File settings
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {".pdf"}
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Processing settings
MAX_BATCH_SIZE = 100
EXTRACT_IMAGES = False
EXTRACT_TABLES = True
EXTRACT_TEXT = True

# API settings
API_PREFIX = "/api"
API_TIMEOUT = 300  # 5 minutes
