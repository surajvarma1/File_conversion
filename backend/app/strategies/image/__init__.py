"""Image strategies package."""

from .strategies import (
    JpgToPngStrategy,
    PngToJpgStrategy,
    WebpToJpgStrategy,
    JpgToWebpStrategy,
    ResizeImageStrategy,
    CompressImageStrategy,
)

__all__ = [
    "JpgToPngStrategy",
    "PngToJpgStrategy",
    "WebpToJpgStrategy",
    "JpgToWebpStrategy",
    "ResizeImageStrategy",
    "CompressImageStrategy",
]
