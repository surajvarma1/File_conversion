"""File validation and security utilities."""

import mimetypes
from pathlib import Path
from typing import Optional

from app.core.config import Settings
from app.core.exceptions import (
    FileValidationError,
    FileSizeError,
    InvalidFormatError,
    CorruptedFileError,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


class FileValidator:
    """File validator."""

    # File signatures (magic bytes)
    MAGIC_BYTES = {
        b"\xff\xd8\xff": "jpg",
        b"\x89PNG\r\n\x1a\n": "png",
        b"RIFF": "webp",
        b"GIF8": "gif",
        b"BM": "bmp",
        b"%PDF": "pdf",
        b"PK\x03\x04": "zip",
    }

    EXECUTABLE_EXTENSIONS = {
        ".exe", ".bat", ".cmd", ".msi", ".scr", ".vbs", ".js",
        ".ps1", ".sh", ".bash", ".py", ".pyc", ".pyo", ".class",
    }

    def __init__(self, settings: Settings):
        """Initialize validator.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.max_size = settings.MAX_UPLOAD_SIZE
        self.allowed_images = set(settings.ALLOWED_IMAGE_FORMATS)
        self.allowed_pdfs = set(settings.ALLOWED_PDF_EXTENSIONS)
        self.allowed_zips = set(settings.ALLOWED_ZIP_EXTENSIONS)

    async def validate_image(self, file_path: Path) -> bool:
        """Validate image file.
        
        Args:
            file_path: Path to image file
            
        Returns:
            True if valid
            
        Raises:
            FileValidationError: If validation fails
        """
        # Check existence
        if not file_path.exists():
            raise FileValidationError("File does not exist")

        # Check size
        self._check_file_size(file_path)

        # Check extension
        ext = file_path.suffix.lower().lstrip(".")
        if ext not in self.allowed_images:
            raise InvalidFormatError(
                f"Invalid image format: {ext}. "
                f"Allowed formats: {', '.join(self.allowed_images)}"
            )

        # Check magic bytes
        self._check_magic_bytes(file_path, ["jpg", "jpeg", "png", "webp", "gif", "bmp"])

        # Check MIME type
        self._check_mime_type(file_path, "image")
        # Optional virus-scan hook (placeholder for integration)
        await self._virus_scan_hook(file_path)

        logger.info(f"Image validation successful: {file_path.name}")
        return True

    async def validate_pdf(self, file_path: Path) -> bool:
        """Validate PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            True if valid
            
        Raises:
            FileValidationError: If validation fails
        """
        if not file_path.exists():
            raise FileValidationError("File does not exist")

        self._check_file_size(file_path)

        ext = file_path.suffix.lower().lstrip(".")
        if ext not in self.allowed_pdfs:
            raise InvalidFormatError(f"Invalid PDF format: {ext}")

        self._check_magic_bytes(file_path, ["pdf"])
        self._check_mime_type(file_path, "application/pdf")
        await self._virus_scan_hook(file_path)

        logger.info(f"PDF validation successful: {file_path.name}")
        return True

    async def validate_zip(self, file_path: Path) -> bool:
        """Validate ZIP file.
        
        Args:
            file_path: Path to ZIP file
            
        Returns:
            True if valid
            
        Raises:
            FileValidationError: If validation fails
        """
        if not file_path.exists():
            raise FileValidationError("File does not exist")

        self._check_file_size(file_path)

        ext = file_path.suffix.lower().lstrip(".")
        if ext not in self.allowed_zips:
            raise InvalidFormatError(f"Invalid ZIP format: {ext}")

        self._check_magic_bytes(file_path, ["zip"])
        self._check_mime_type(file_path, "application/zip")

        # Check if ZIP is corrupted
        import zipfile
        try:
            with zipfile.ZipFile(file_path, "r") as zip_file:
                bad_file = zip_file.testzip()
                if bad_file:
                    raise CorruptedFileError(
                        f"ZIP file is corrupted. Bad file: {bad_file}"
                    )
        except zipfile.BadZipFile:
            raise CorruptedFileError("Invalid or corrupted ZIP file")

        logger.info(f"ZIP validation successful: {file_path.name}")
        await self._virus_scan_hook(file_path)
        return True

    def _check_file_size(self, file_path: Path) -> None:
        """Check file size.
        
        Args:
            file_path: Path to file
            
        Raises:
            FileSizeError: If file is too large
        """
        size = file_path.stat().st_size
        if size > self.max_size:
            raise FileSizeError(
                f"File size {size} bytes exceeds maximum {self.max_size} bytes"
            )
        if size == 0:
            raise FileValidationError("File is empty")

    def _check_magic_bytes(self, file_path: Path, expected_types: list[str]) -> None:
        """Check file magic bytes.
        
        Args:
            file_path: Path to file
            expected_types: Expected file types
            
        Raises:
            CorruptedFileError: If magic bytes don't match
        """
        try:
            with open(file_path, "rb") as f:
                header = f.read(12)

            detected_type = None
            for magic_bytes, file_type in self.MAGIC_BYTES.items():
                if header.startswith(magic_bytes):
                    detected_type = file_type
                    break

            if detected_type not in expected_types:
                raise CorruptedFileError(
                    f"File signature does not match expected format. "
                    f"Expected: {expected_types}, Got: {detected_type}"
                )
        except (IOError, OSError) as e:
            raise CorruptedFileError(f"Cannot read file: {str(e)}")

    def _check_mime_type(self, file_path: Path, expected_mime: str) -> None:
        """Check MIME type.
        
        Args:
            file_path: Path to file
            expected_mime: Expected MIME type
            
        Raises:
            InvalidFormatError: If MIME type doesn't match
        """
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if mime_type and expected_mime not in mime_type:
            logger.warning(
                f"MIME type mismatch. Expected: {expected_mime}, Got: {mime_type}"
            )

    def is_executable(self, file_path: Path) -> bool:
        """Check if file is executable.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if executable, False otherwise
        """
        return file_path.suffix.lower() in self.EXECUTABLE_EXTENSIONS

    async def _virus_scan_hook(self, file_path: Path) -> bool:
        """Placeholder hook for virus scanning integration.

        Integrate ClamAV, commercial scanner, or external virus-scanning service here.
        Currently logs and returns True.
        """
        try:
            logger.info(f"Running virus-scan hook for {file_path.name} (placeholder)")
            # TODO: call external scanner and raise CorruptedFileError if infected
            return True
        except Exception as e:
            logger.error(f"Virus scan hook failed: {str(e)}")
            return True
