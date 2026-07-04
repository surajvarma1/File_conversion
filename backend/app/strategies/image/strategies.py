"""Image conversion strategies."""

import io
from pathlib import Path
from typing import Optional

from PIL import Image

from app.core.exceptions import ConversionError
from app.core.logging import get_logger

logger = get_logger(__name__)


class ImageConversionStrategy:
    """Base image conversion strategy."""

    async def convert(self, input_file: Path, output_file: Path, **kwargs) -> Path:
        """Convert image.
        
        Args:
            input_file: Path to input image
            output_file: Path to output image
            **kwargs: Conversion options
            
        Returns:
            Path to output file
            
        Raises:
            ConversionError: If conversion fails
        """
        raise NotImplementedError


class JpgToPngStrategy(ImageConversionStrategy):
    """JPG to PNG conversion strategy."""

    async def convert(self, input_file: Path, output_file: Path, **kwargs) -> Path:
        """Convert JPG to PNG."""
        try:
            with Image.open(input_file) as img:
                # Convert RGBA if needed
                if img.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
                    background.save(output_file, "PNG", quality=95)
                else:
                    img.save(output_file, "PNG", quality=95)
            logger.info(f"JPG to PNG conversion successful: {input_file.name}")
            return output_file
        except Exception as e:
            logger.error(f"JPG to PNG conversion failed: {str(e)}")
            raise ConversionError(f"Failed to convert JPG to PNG: {str(e)}")


class PngToJpgStrategy(ImageConversionStrategy):
    """PNG to JPG conversion strategy."""

    async def convert(self, input_file: Path, output_file: Path, **kwargs) -> Path:
        """Convert PNG to JPG."""
        try:
            with Image.open(input_file) as img:
                # Convert RGBA to RGB
                if img.mode in ("RGBA", "LA", "P"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                    img = background

                quality = kwargs.get("quality", 85)
                img.save(output_file, "JPEG", quality=quality, optimize=True)
            logger.info(f"PNG to JPG conversion successful: {input_file.name}")
            return output_file
        except Exception as e:
            logger.error(f"PNG to JPG conversion failed: {str(e)}")
            raise ConversionError(f"Failed to convert PNG to JPG: {str(e)}")


class WebpToJpgStrategy(ImageConversionStrategy):
    """WebP to JPG conversion strategy."""

    async def convert(self, input_file: Path, output_file: Path, **kwargs) -> Path:
        """Convert WebP to JPG."""
        try:
            with Image.open(input_file) as img:
                # Convert RGBA to RGB if needed
                if img.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                quality = kwargs.get("quality", 85)
                img.save(output_file, "JPEG", quality=quality, optimize=True)
            logger.info(f"WebP to JPG conversion successful: {input_file.name}")
            return output_file
        except Exception as e:
            logger.error(f"WebP to JPG conversion failed: {str(e)}")
            raise ConversionError(f"Failed to convert WebP to JPG: {str(e)}")


class JpgToWebpStrategy(ImageConversionStrategy):
    """JPG to WebP conversion strategy."""

    async def convert(self, input_file: Path, output_file: Path, **kwargs) -> Path:
        """Convert JPG to WebP."""
        try:
            with Image.open(input_file) as img:
                quality = kwargs.get("quality", 80)
                img.save(output_file, "WEBP", quality=quality, method=6)
            logger.info(f"JPG to WebP conversion successful: {input_file.name}")
            return output_file
        except Exception as e:
            logger.error(f"JPG to WebP conversion failed: {str(e)}")
            raise ConversionError(f"Failed to convert JPG to WebP: {str(e)}")


class ResizeImageStrategy(ImageConversionStrategy):
    """Image resize strategy."""

    async def convert(
        self, input_file: Path, output_file: Path, **kwargs
    ) -> Path:
        """Resize image.
        
        Args:
            input_file: Path to input image
            output_file: Path to output image
            **kwargs: Must include 'width' and 'height'
        """
        try:
            width = kwargs.get("width")
            height = kwargs.get("height")
            maintain_aspect = kwargs.get("maintain_aspect", True)

            if not width or not height:
                raise ValueError("Width and height are required")

            with Image.open(input_file) as img:
                if maintain_aspect:
                    img.thumbnail((int(width), int(height)), Image.Resampling.LANCZOS)
                else:
                    img = img.resize((int(width), int(height)), Image.Resampling.LANCZOS)

                # Convert to RGB if needed
                if img.mode in ("RGBA", "LA", "P"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                    img = background

                format_type = output_file.suffix.upper().lstrip(".")
                img.save(output_file, format=format_type, quality=90, optimize=True)

            logger.info(f"Image resize successful: {input_file.name} -> {width}x{height}")
            return output_file
        except Exception as e:
            logger.error(f"Image resize failed: {str(e)}")
            raise ConversionError(f"Failed to resize image: {str(e)}")


class CompressImageStrategy(ImageConversionStrategy):
    """Image compress strategy."""

    async def convert(
        self, input_file: Path, output_file: Path, **kwargs
    ) -> Path:
        """Compress image.
        
        Args:
            input_file: Path to input image
            output_file: Path to output image
            **kwargs: May include 'quality'
        """
        try:
            quality = kwargs.get("quality", 75)
            max_size = kwargs.get("max_size")
            


            with Image.open(input_file) as img:
                # Convert to RGB if needed for JPEG
                if img.mode in ("RGBA", "LA", "P"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    background.paste(img, mask=img.split()[-1] if "A" in img.mode else None)
                    img = background

                # format_type = output_file.suffix.upper().lstrip(".")
                format_type = img.format

                # Compress iteratively if max_size is specified
                if max_size:
                    quality_level = quality
                    while quality_level > 10:
                        img.save(output_file, format=format_type, quality=quality_level, optimize=True)
                        if output_file.stat().st_size <= max_size*1024: # max size in Kb
                            break
                        quality_level -= 5
                else:
                    img.save(output_file, format=format_type, quality=quality, optimize=True)

            logger.info(f"Image compression successful: {input_file.name}")
            return output_file
        except Exception as e:
            logger.error(f"Image compression failed: {str(e)}")
            raise ConversionError(f"Failed to compress image: {str(e)}")
