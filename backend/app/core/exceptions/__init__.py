"""Exceptions package."""

from .exceptions import (
    AppException,
    FileValidationError,
    ConversionError,
    StorageError,
    NotFoundError,
    InvalidFormatError,
    FileSizeError,
    CorruptedFileError,
)

__all__ = [
    "AppException",
    "FileValidationError",
    "ConversionError",
    "StorageError",
    "NotFoundError",
    "InvalidFormatError",
    "FileSizeError",
    "CorruptedFileError",
]
