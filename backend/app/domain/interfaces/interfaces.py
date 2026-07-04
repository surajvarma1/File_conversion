"""Domain interfaces."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class ConversionStrategy(ABC):
    """Base conversion strategy interface."""

    @abstractmethod
    async def execute(self, input_file: Path, **kwargs) -> Path:
        """Execute conversion.
        
        Args:
            input_file: Path to input file
            **kwargs: Conversion options
            
        Returns:
            Path to output file
            
        Raises:
            ConversionError: If conversion fails
        """
        pass


class ImageConversionStrategy(ConversionStrategy):
    """Image conversion strategy interface."""

    @abstractmethod
    async def execute(
        self, input_file: Path, output_file: Path, **kwargs
    ) -> Path:
        """Execute image conversion."""
        pass


class PdfStrategy(ConversionStrategy):
    """PDF operation strategy interface."""

    @abstractmethod
    async def execute(self, input_files: list[Path], **kwargs) -> Path:
        """Execute PDF operation."""
        pass


class ZipStrategy(ConversionStrategy):
    """ZIP operation strategy interface."""

    @abstractmethod
    async def execute(self, input_file: Path, output_dir: Path) -> Path:
        """Execute ZIP operation."""
        pass


class FileValidator(ABC):
    """File validation interface."""

    @abstractmethod
    async def validate(self, file_path: Path) -> bool:
        """Validate file.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            FileValidationError: If validation fails
        """
        pass


class FileStorage(ABC):
    """File storage interface."""

    @abstractmethod
    async def save(self, file_path: Path, destination: str) -> str:
        """Save file.
        
        Args:
            file_path: Path to file
            destination: Destination path
            
        Returns:
            File URL or path
        """
        pass

    @abstractmethod
    async def retrieve(self, file_id: str) -> Path:
        """Retrieve file.
        
        Args:
            file_id: File identifier
            
        Returns:
            Path to file
        """
        pass

    @abstractmethod
    async def delete(self, file_id: str) -> bool:
        """Delete file.
        
        Args:
            file_id: File identifier
            
        Returns:
            True if deleted successfully
        """
        pass
