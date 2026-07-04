"""File storage service."""

import os
import shutil
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import time
import hmac
import hashlib
import urllib.parse

from app.core.config import Settings
from app.core.exceptions import StorageError
from app.core.logging import get_logger

logger = get_logger(__name__)


class LocalFileStorage:
    """Local file storage implementation."""

    def __init__(self, settings: Settings):
        """Initialize storage.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.upload_dir = settings.UPLOAD_DIR
        self.output_dir = settings.OUTPUT_DIR
        self.temp_dir = settings.TEMP_DIR

        # Create directories
        for dir_path in [self.upload_dir, self.output_dir, self.temp_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def generate_file_id(self) -> str:
        """Generate unique file ID.
        
        Returns:
            Unique file ID
        """
        return str(uuid.uuid4())

    async def save_upload(self, file_path: Path, original_filename: str) -> str:
        """Save uploaded file.
        
        Args:
            file_path: Path to file to save
            original_filename: Original filename
            
        Returns:
            File ID
            
        Raises:
            StorageError: If save fails
        """
        try:
            file_id = self.generate_file_id()
            file_ext = Path(original_filename).suffix

            # Save to uploads directory
            saved_path = self.upload_dir / f"{file_id}{file_ext}"
            shutil.copy2(file_path, saved_path)

            logger.info(f"File saved: {file_id}{file_ext}")
            return file_id
        except Exception as e:
            logger.error(f"Failed to save file: {str(e)}")
            raise StorageError(f"Failed to save file: {str(e)}")

    async def save_output(self, file_path: Path, original_filename: str) -> str:
        """Save output file.
        
        Args:
            file_path: Path to file to save
            original_filename: Original filename
            
        Returns:
            File ID
            
        Raises:
            StorageError: If save fails
        """
        try:
            file_id = self.generate_file_id()
            file_ext = Path(original_filename).suffix

            saved_path = self.output_dir / f"{file_id}{file_ext}"
            shutil.copy2(file_path, saved_path)

            logger.info(f"Output file saved: {file_id}{file_ext}")
            return file_id
        except Exception as e:
            logger.error(f"Failed to save output file: {str(e)}")
            raise StorageError(f"Failed to save output file: {str(e)}")

    async def retrieve(self, file_id: str, file_dir: Path) -> Optional[Path]:
        """Retrieve file.
        
        Args:
            file_id: File ID
            file_dir: Directory to search in
            
        Returns:
            Path to file if found, None otherwise
        """
        try:
            # Search for file with any extension
            for file_path in file_dir.iterdir():
                if file_path.name.startswith(file_id):
                    return file_path
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve file: {str(e)}")
            return None

    async def delete(self, file_id: str, file_dir: Path) -> bool:
        """Delete file.
        
        Args:
            file_id: File ID
            file_dir: Directory containing file
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            file_path = await self.retrieve(file_id, file_dir)
            if file_path and file_path.exists():
                file_path.unlink()
                logger.info(f"File deleted: {file_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file: {str(e)}")
            return False

    async def cleanup_old_files(self, ttl_seconds: int) -> int:
        """Clean up old temporary files.
        
        Args:
            ttl_seconds: Time to live in seconds
            
        Returns:
            Number of files deleted
        """
        try:
            deleted_count = 0
            cutoff_time = datetime.now() - timedelta(seconds=ttl_seconds)

            for dir_path in [self.temp_dir, self.upload_dir]:
                if dir_path.exists():
                    for file_path in dir_path.iterdir():
                        if file_path.is_file():
                            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                            if mtime < cutoff_time:
                                file_path.unlink()
                                deleted_count += 1
                                logger.info(f"Cleaned up old file: {file_path.name}")

            logger.info(f"Cleanup complete. Deleted {deleted_count} files")
            return deleted_count
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            return 0

    def generate_presigned_url(self, filename: str, expires_in: int = 3600) -> str:
        """Generate a simple presigned URL for local files.

        Note: This is optimized for local deployments. In production, use storage provider
        presigned URLs (S3, GCS) or a secure CDN.
        """
        expiry = int(time.time()) + int(expires_in)
        message = f"{filename}|{expiry}"
        secret = str(self.settings.SECRET_KEY).encode()
        signature = hmac.new(secret, message.encode(), hashlib.sha256).hexdigest()
        qs = urllib.parse.urlencode({"filename": filename, "expires": expiry, "sig": signature})
        return f"{self.settings.API_V1_STR}/download/serve?{qs}"

    def verify_presigned(self, filename: str, expires: int, sig: str) -> bool:
        try:
            expiry = int(expires)
            if int(time.time()) > expiry:
                return False
            message = f"{filename}|{expiry}"
            secret = str(self.settings.SECRET_KEY).encode()
            expected = hmac.new(secret, message.encode(), hashlib.sha256).hexdigest()
            return hmac.compare_digest(expected, sig)
        except Exception:
            return False
