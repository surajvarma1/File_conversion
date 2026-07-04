"""Domain entities."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class File:
    """File entity."""

    file_id: str
    filename: str
    file_type: str
    file_size: int
    mime_type: str
    path: Path
    created_at: datetime
    metadata: Optional[dict] = None


@dataclass
class ConversionJob:
    """Conversion job entity."""

    job_id: str
    input_file: File
    output_file: Optional[File]
    conversion_type: str
    status: str  # pending, processing, completed, failed
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime] = None
    processing_time: Optional[float] = None
    options: Optional[dict] = None


@dataclass
class ValidationResult:
    """File validation result."""

    is_valid: bool
    message: str
    file_format: Optional[str] = None
    file_size: Optional[int] = None
