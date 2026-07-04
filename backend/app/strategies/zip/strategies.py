"""ZIP manipulation strategies."""

import shutil
import zipfile
from pathlib import Path

from app.core.exceptions import ConversionError
from app.core.logging import get_logger

logger = get_logger(__name__)


class ExtractZipStrategy:
    """ZIP extraction strategy."""

    async def execute(
        self, input_file: Path, output_dir: Path, **kwargs
    ) -> Path:
        """Extract ZIP file.
        
        Args:
            input_file: Path to ZIP file
            output_dir: Directory for extracted files
            **kwargs: Additional options
            
        Returns:
            Path to extraction directory
            
        Raises:
            ConversionError: If extraction fails
        """
        try:
            if not input_file.exists():
                raise ConversionError("ZIP file not found")

            output_dir.mkdir(parents=True, exist_ok=True)

            # Security check: prevent zip bombs and path traversal
            max_archive_size = kwargs.get("max_archive_size", 500 * 1024 * 1024)  # 500MB
            max_file_size = kwargs.get("max_file_size", 100 * 1024 * 1024)  # 100MB

            with zipfile.ZipFile(input_file, "r") as zip_ref:
                # Validate archive before extraction
                self._validate_zip_archive(zip_ref, max_archive_size, max_file_size)

                # Extract safely
                for member in zip_ref.namelist():
                    # Security: prevent directory traversal
                    member_path = Path(output_dir) / member
                    if not str(member_path.resolve()).startswith(str(output_dir.resolve())):
                        raise ConversionError(
                            f"Attempted path traversal in ZIP file: {member}"
                        )

                zip_ref.extractall(output_dir)

            logger.info(f"ZIP extraction successful: {input_file.name}")
            return output_dir
        except zipfile.BadZipFile as e:
            logger.error(f"ZIP extraction failed: Invalid ZIP file - {str(e)}")
            raise ConversionError(f"Invalid or corrupted ZIP file: {str(e)}")
        except Exception as e:
            logger.error(f"ZIP extraction failed: {str(e)}")
            raise ConversionError(f"Failed to extract ZIP file: {str(e)}")

    def _validate_zip_archive(
        self, zip_file: zipfile.ZipFile, max_archive_size: int, max_file_size: int
    ) -> None:
        """Validate ZIP archive for security issues.
        
        Args:
            zip_file: ZIP file object
            max_archive_size: Maximum archive size
            max_file_size: Maximum individual file size
            
        Raises:
            ConversionError: If validation fails
        """
        # Check total uncompressed size
        total_size = sum(info.file_size for info in zip_file.infolist())
        if total_size > max_archive_size:
            raise ConversionError(
                f"ZIP archive too large: {total_size} > {max_archive_size}"
            )

        # Check individual file sizes
        for info in zip_file.infolist():
            if info.file_size > max_file_size:
                raise ConversionError(
                    f"File in ZIP too large: {info.filename} ({info.file_size} bytes)"
                )

            # Check for suspicious filenames
            if ".." in info.filename or info.filename.startswith("/"):
                raise ConversionError(f"Suspicious filename in ZIP: {info.filename}")
