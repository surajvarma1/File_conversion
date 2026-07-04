"""Strategy factories."""

from pathlib import Path
from typing import Dict, Type

from app.core.exceptions import ConversionError
from app.strategies.image import (
    JpgToPngStrategy,
    PngToJpgStrategy,
    WebpToJpgStrategy,
    JpgToWebpStrategy,
    ResizeImageStrategy,
    CompressImageStrategy,
)
from app.strategies.pdf import (
    MergePdfStrategy,
    SplitPdfStrategy,
    ImagesToPdfStrategy,
)
from app.strategies.zip import ExtractZipStrategy


class ImageStrategyFactory:
    """Factory for image conversion strategies."""

    _strategies: Dict[str, Type] = {
        "jpg_to_png": JpgToPngStrategy,
        "png_to_jpg": PngToJpgStrategy,
        "webp_to_jpg": WebpToJpgStrategy,
        "jpg_to_webp": JpgToWebpStrategy,
        "resize": ResizeImageStrategy,
        "compress": CompressImageStrategy,
    }

    @classmethod
    def get_strategy(cls, strategy_name: str):
        """Get image conversion strategy.
        
        Args:
            strategy_name: Name of the strategy
            
        Returns:
            Strategy instance
            
        Raises:
            ConversionError: If strategy not found
        """
        strategy_class = cls._strategies.get(strategy_name)
        if not strategy_class:
            raise ConversionError(
                f"Unknown image strategy: {strategy_name}. "
                f"Available: {', '.join(cls._strategies.keys())}"
            )
        return strategy_class()

    @classmethod
    def register_strategy(cls, name: str, strategy_class: Type) -> None:
        """Register new strategy.
        
        Args:
            name: Strategy name
            strategy_class: Strategy class
        """
        cls._strategies[name] = strategy_class


class PdfStrategyFactory:
    """Factory for PDF strategies."""

    _strategies: Dict[str, Type] = {
        "merge": MergePdfStrategy,
        "split": SplitPdfStrategy,
        "images_to_pdf": ImagesToPdfStrategy,
    }

    @classmethod
    def get_strategy(cls, strategy_name: str):
        """Get PDF strategy.
        
        Args:
            strategy_name: Name of the strategy
            
        Returns:
            Strategy instance
            
        Raises:
            ConversionError: If strategy not found
        """
        strategy_class = cls._strategies.get(strategy_name)
        if not strategy_class:
            raise ConversionError(
                f"Unknown PDF strategy: {strategy_name}. "
                f"Available: {', '.join(cls._strategies.keys())}"
            )
        return strategy_class()

    @classmethod
    def register_strategy(cls, name: str, strategy_class: Type) -> None:
        """Register new strategy.
        
        Args:
            name: Strategy name
            strategy_class: Strategy class
        """
        cls._strategies[name] = strategy_class


class ZipStrategyFactory:
    """Factory for ZIP strategies."""

    _strategies: Dict[str, Type] = {
        "extract": ExtractZipStrategy,
    }

    @classmethod
    def get_strategy(cls, strategy_name: str):
        """Get ZIP strategy.
        
        Args:
            strategy_name: Name of the strategy
            
        Returns:
            Strategy instance
            
        Raises:
            ConversionError: If strategy not found
        """
        strategy_class = cls._strategies.get(strategy_name)
        if not strategy_class:
            raise ConversionError(
                f"Unknown ZIP strategy: {strategy_name}. "
                f"Available: {', '.join(cls._strategies.keys())}"
            )
        return strategy_class()

    @classmethod
    def register_strategy(cls, name: str, strategy_class: Type) -> None:
        """Register new strategy.
        
        Args:
            name: Strategy name
            strategy_class: Strategy class
        """
        cls._strategies[name] = strategy_class
