"""Application DTOs."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ConversionRequest:
    """Base conversion request DTO."""

    file_id: str
    output_format: str
    options: Optional[dict] = None


@dataclass
class ImageConversionRequest(ConversionRequest):
    """Image conversion request DTO."""

    quality: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    maintain_aspect: bool = True


@dataclass
class ConversionResponse:
    """Conversion response DTO."""

    success: bool
    message: str
    output_file_id: Optional[str] = None
    output_filename: Optional[str] = None
    processing_time: Optional[float] = None
    error_code: Optional[str] = None
