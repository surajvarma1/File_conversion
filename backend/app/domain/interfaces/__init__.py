"""Domain interfaces package."""

from .interfaces import (
    ConversionStrategy,
    ImageConversionStrategy,
    PdfStrategy,
    ZipStrategy,
    FileValidator,
    FileStorage,
)

__all__ = [
    "ConversionStrategy",
    "ImageConversionStrategy",
    "PdfStrategy",
    "ZipStrategy",
    "FileValidator",
    "FileStorage",
]
