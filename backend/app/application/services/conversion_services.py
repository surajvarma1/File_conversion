"""Application services."""

from pathlib import Path
from typing import List, Optional

from app.core.config import Settings
from app.core.exceptions import ConversionError
from app.core.logging import get_logger
from app.core.security import FileValidator
from app.infrastructure.converters import (
    ImageStrategyFactory,
    PdfStrategyFactory,
    ZipStrategyFactory,
)
from app.infrastructure.file_storage import LocalFileStorage
from app.schemas.image_schemas import ImageResizeSchema

logger = get_logger(__name__)


class ImageConversionService:
    """Image conversion service."""

    def __init__(self, settings: Settings, file_storage: LocalFileStorage, validator: FileValidator):
        """Initialize service.
        
        Args:
            settings: Application settings
            file_storage: File storage instance
            validator: File validator instance
        """
        self.settings = settings
        self.file_storage = file_storage
        self.validator = validator
        self.factory = ImageStrategyFactory()

    async def convert_jpg_to_png(self, input_file: Path, output_file: Path) -> Path:
        """Convert JPG to PNG."""
        await self.validator.validate_image(input_file)
        strategy = self.factory.get_strategy("jpg_to_png")
        return await strategy.convert(input_file, output_file)

    async def convert_png_to_jpg(
        self, input_file: Path, output_file: Path, quality: int = 85
    ) -> Path:
        """Convert PNG to JPG."""
        await self.validator.validate_image(input_file)
        strategy = self.factory.get_strategy("png_to_jpg")
        return await strategy.convert(input_file, output_file, quality=quality)

    async def convert_webp_to_jpg(
        self, input_file: Path, output_file: Path, quality: int = 85
    ) -> Path:
        """Convert WebP to JPG."""
        await self.validator.validate_image(input_file)
        strategy = self.factory.get_strategy("webp_to_jpg")
        return await strategy.convert(input_file, output_file, quality=quality)

    async def convert_jpg_to_webp(
        self, input_file: Path, output_file: Path, quality: int = 80
    ) -> Path:
        """Convert JPG to WebP."""
        await self.validator.validate_image(input_file)
        strategy = self.factory.get_strategy("jpg_to_webp")
        return await strategy.convert(input_file, output_file, quality=quality)

    # async def resize_image(
    #     self,
    #     input_file: Path,
    #     output_file: Path,
    #     width: int,
    #     height: int,
    #     maintain_aspect: bool = True,
    # ) -> Path:
    #     """Resize image."""
    #     await self.validator.validate_image(input_file)
    #     strategy = self.factory.get_strategy("resize")
    #     return await strategy.convert(
    #         input_file,
    #         output_file,
    #         width=width,
    #         height=height,
    #         maintain_aspect=maintain_aspect,
    #     )

    async def resize_image(
        self,
        input_file: Path,
        output_file: Path,
        payload: "ImageResizeSchema",
    ) -> Path:
        """Advanced resize image orchestrator handling formats and sizes."""
        await self.validator.validate_image(input_file)
        
        # We fetch the resize strategy. 
        # Note: Your underlying converter (e.g., in ImageStrategyFactory) 
        # will need to be updated to accept and process these new kwargs.
        strategy = self.factory.get_strategy("resize")
        
        return await strategy.convert(
            input_file,
            output_file,
            resize_mode=payload.resize_mode,
            width=payload.width,
            height=payload.height,
            maintain_aspect=payload.maintain_aspect,
            percentage=payload.percentage,
            social_media_preset=payload.social_media_preset,
            target_size_kb=payload.target_size_kb,
            output_format=payload.output_format
        )

    async def compress_image(
        self,
        input_file: Path,
        output_file: Path,
        quality: int = 75,
        max_size: Optional[int] = None,
    ) -> Path:
        """Compress image."""
        await self.validator.validate_image(input_file)
        strategy = self.factory.get_strategy("compress")
        return await strategy.convert(
            input_file, output_file, quality=quality, max_size=max_size
        )


# class PdfService:
#     """PDF service."""

#     def __init__(self, settings: Settings, file_storage: LocalFileStorage, validator: FileValidator):
#         """Initialize service.
        
#         Args:
#             settings: Application settings
#             file_storage: File storage instance
#             validator: File validator instance
#         """
#         self.settings = settings
#         self.file_storage = file_storage
#         self.validator = validator
#         self.factory = PdfStrategyFactory()

#     async def merge_pdf(self, input_files: List[Path], output_file: Path) -> Path:
#         """Merge PDFs."""
#         for file in input_files:
#             await self.validator.validate_pdf(file)
#         strategy = self.factory.get_strategy("merge")
#         return await strategy.execute(input_files, output_file)

   

#     # async def split_pdf(
#     #     self, 
#     #     input_file: Path, 
#     #     output_dir: Path, 
#     #     pages: Optional[str] = None,
#     #     split_mode: str = "specific"  # Added this parameter
#     # ) -> Path:
#     #     """Split PDF."""
#     #     await self.validator.validate_pdf(input_file)
#     #     strategy = self.factory.get_strategy("split")
        
#     #     # Pass the split_mode down to the underlying strategy execution
#     #     return await strategy.execute(
#     #         input_file, 
#     #         output_dir, 
#     #         pages=pages, 
#     #         split_mode=split_mode
#     #     )

#     from pypdf import PdfReader, PdfWriter

#     async def split_pdf(self, input_file: Path, output_file: Path, pages: List[int], split_mode):
#         reader = PdfReader(input_file)
#         writer = PdfWriter()

#         # Subtract 1 from page numbers because Python lists are 0-indexed
#         for page_num in pages:
#             if 0 <= (page_num - 1) < len(reader.pages):
#                 writer.add_page(reader.pages[page_num - 1])

#         # Save all extracted pages into ONE single new PDF
#         with open(output_file, "wb") as out_pdf:
#             writer.write(out_pdf)
            
#         return output_file

from pypdf import PdfReader, PdfWriter  # Moved import to the top of this section
from PIL import Image

class PdfService:
    """PDF service."""

    def __init__(self, settings: Settings, file_storage: LocalFileStorage, validator: FileValidator):
        """Initialize service.
        
        Args:
            settings: Application settings
            file_storage: File storage instance
            validator: File validator instance
        """
        self.settings = settings
        self.file_storage = file_storage
        self.validator = validator
        self.factory = PdfStrategyFactory()

    async def merge_pdf(self, input_files: List[Path], output_file: Path) -> Path:
        """Merge PDFs."""
        for file in input_files:
            await self.validator.validate_pdf(file)
        strategy = self.factory.get_strategy("merge")
        return await strategy.execute(input_files, output_file)

    # # Indented to be INSIDE the class!
    # async def split_pdf(self, input_file: Path, output_file: Path, pages: any, split_mode: str):
    #     reader = PdfReader(input_file)
    #     writer = PdfWriter()

    #     # 1. Safely parse the pages input into a list of integers
    #     page_numbers = []
    #     if isinstance(pages, str):
    #         # If it's a string like "1,2", split by comma and convert to ints
    #         page_numbers = [int(p.strip()) for p in pages.split(",")]
    #     elif isinstance(pages, list):
    #         # If FastAPI already parsed it as a list, just ensure they are ints
    #         page_numbers = [int(p) for p in pages]
    #     else:
    #         # Fallback for a single number
    #         page_numbers = [int(pages)]

    #     # 2. Now loop through the clean list of integers
    #     for page_num in page_numbers:
    #         index = page_num - 1
            
    #         # Ensure the page exists to prevent crashes
    #         if 0 <= index < len(reader.pages):
    #             writer.add_page(reader.pages[index])

    #     # 3. Save the new PDF
    #     with open(output_file, "wb") as out_pdf:
    #         writer.write(out_pdf)
            
    #     return output_file
    async def split_pdf(self, input_file: Path, output_file: Path, pages: any, split_mode: str):
        reader = PdfReader(input_file)
        writer = PdfWriter()
        total_pages = len(reader.pages)

        page_numbers = []

        # 1. SPECIFIC PAGES (Logic kept exactly as it was)
        if split_mode == "specific":
            if isinstance(pages, str):
                page_numbers = [int(p.strip()) for p in pages.split(",")]
            elif isinstance(pages, list):
                page_numbers = [int(p) for p in pages]
            elif pages is not None:
                page_numbers = [int(pages)]

        # 2. PAGE RANGE (e.g., "1-5")
        elif split_mode == "range":
            if isinstance(pages, str) and "-" in pages:
                start_str, end_str = pages.split("-")
                start = int(start_str.strip())
                end = int(end_str.strip())
                # Generate a list of numbers from start to end (inclusive)
                page_numbers = list(range(start, end + 1))

        # 3. EVEN PAGES ONLY
        elif split_mode == "even":
            # Generate: 2, 4, 6, 8... up to the total number of pages
            page_numbers = [p for p in range(1, total_pages + 1) if p % 2 == 0]

        # 4. ODD PAGES ONLY
        elif split_mode == "odd":
            # Generate: 1, 3, 5, 7... up to the total number of pages
            page_numbers = [p for p in range(1, total_pages + 1) if p % 2 != 0]

        # Process the calculated page numbers
        for page_num in page_numbers:
            index = page_num - 1
            
            # Ensure the page exists to prevent crashes
            if 0 <= index < total_pages:
                writer.add_page(reader.pages[index])

        # Save the new single PDF
        with open(output_file, "wb") as out_pdf:
            writer.write(out_pdf)
            
        return output_file
    
    async def images_to_pdf(self, input_files: List[Path], output_file: Path) -> Path:
        """
        Converts a list of image files into a single PDF document.
        """
        if not input_files:
            raise ValueError("No input files provided for conversion.")

        # Open the first image and convert it to standard RGB 
        # (PDFs do not support alpha channels / transparency like PNGs do)
        first_image = Image.open(input_files[0]).convert("RGB")
        
        # Process the remaining images in the list
        additional_images = []
        for file_path in input_files[1:]:
            img = Image.open(file_path).convert("RGB")
            additional_images.append(img)
            
        # Save the first image as a PDF and append the rest of the list
        first_image.save(
            output_file, 
            "PDF", 
            resolution=100.0, 
            save_all=True, 
            append_images=additional_images
        )
        
        return output_file
    

class ZipService:
    """ZIP service."""

    def __init__(self, settings: Settings, file_storage: LocalFileStorage, validator: FileValidator):
        """Initialize service.
        
        Args:
            settings: Application settings
            file_storage: File storage instance
            validator: File validator instance
        """
        self.settings = settings
        self.file_storage = file_storage
        self.validator = validator
        self.factory = ZipStrategyFactory()

    async def extract_zip(self, input_file: Path, output_dir: Path) -> Path:
        """Extract ZIP."""
        await self.validator.validate_zip(input_file)
        strategy = self.factory.get_strategy("extract")
        return await strategy.execute(input_file, output_dir)
