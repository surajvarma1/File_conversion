"""PDF manipulation strategies."""

from pathlib import Path
from typing import List

import img2pdf
from PIL import Image
from pypdf import PdfWriter, PdfReader

from app.core.exceptions import ConversionError
from app.core.logging import get_logger

logger = get_logger(__name__)


class PdfStrategy:
    """Base PDF strategy."""

    async def execute(self, *args, **kwargs) -> Path:
        """Execute PDF operation."""
        raise NotImplementedError


class MergePdfStrategy(PdfStrategy):
    """PDF merge strategy."""

    async def execute(self, input_files: List[Path], output_file: Path, **kwargs) -> Path:
        """Merge multiple PDFs.
        
        Args:
            input_files: List of paths to PDF files
            output_file: Path to output PDF
            **kwargs: Additional options
            
        Returns:
            Path to output file
            
        Raises:
            ConversionError: If merge fails
        """
        try:
            if not input_files or len(input_files) < 2:
                raise ConversionError("At least 2 PDF files are required for merging")

            pdf_writer = PdfWriter()

            for pdf_file in input_files:
                if not pdf_file.exists():
                    raise ConversionError(f"Input file not found: {pdf_file}")

                pdf_reader = PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

            with open(output_file, "wb") as f:
                pdf_writer.write(f)

            logger.info(f"PDF merge successful: {len(input_files)} files merged")
            return output_file
        except Exception as e:
            logger.error(f"PDF merge failed: {str(e)}")
            raise ConversionError(f"Failed to merge PDFs: {str(e)}")


# class SplitPdfStrategy(PdfStrategy):
#     """PDF split strategy."""

#     async def execute(
#         self,
#         input_file: Path,
#         output_dir: Path,
#         pages: str = None,
#         **kwargs
#     ) -> Path:
#         """Split PDF.
        
#         Args:
#             input_file: Path to input PDF
#             output_dir: Directory for output PDFs
#             pages: Page ranges (e.g., "1-3,5,7-9" or "all")
#             **kwargs: Additional options
            
#         Returns:
#             Path to output directory
            
#         Raises:
#             ConversionError: If split fails
#         """
#         try:
#             if not input_file.exists():
#                 raise ConversionError("Input PDF file not found")

#             output_dir.mkdir(parents=True, exist_ok=True)

#             pdf_reader = PdfReader(input_file)
#             total_pages = len(pdf_reader.pages)

#             # Parse page ranges
#             page_indices = self._parse_page_ranges(pages, total_pages)

#             if not page_indices:
#                 raise ConversionError("No valid pages specified")

#             # Split into individual files
#             for idx, page_idx in enumerate(page_indices, 1):
#                 pdf_writer = PdfWriter()
#                 pdf_writer.add_page(pdf_reader.pages[page_idx])

#                 output_file = output_dir / f"page_{idx:04d}.pdf"
#                 with open(output_file, "wb") as f:
#                     pdf_writer.write(f)

#             logger.info(f"PDF split successful: {len(page_indices)} pages extracted")
#             return output_dir
#         except Exception as e:
#             logger.error(f"PDF split failed: {str(e)}")
#             raise ConversionError(f"Failed to split PDF: {str(e)}")

#     def _parse_page_ranges(self, pages: str, total_pages: int) -> list:
#         """Parse page range string.
        
#         Args:
#             pages: Page range string (e.g., "1-3,5,7-9" or "all")
#             total_pages: Total number of pages
            
#         Returns:
#             List of page indices (0-based)
#         """
#         if pages is None or pages == "all":
#             return list(range(total_pages))

#         page_indices = []
#         parts = pages.split(",")

#         for part in parts:
#             part = part.strip()
#             if "-" in part:
#                 start, end = part.split("-")
#                 start = int(start.strip()) - 1  # Convert to 0-based
#                 end = int(end.strip())  # Keep inclusive
#                 page_indices.extend(range(start, min(end, total_pages)))
#             else:
#                 page_idx = int(part) - 1  # Convert to 0-based
#                 if 0 <= page_idx < total_pages:
#                     page_indices.append(page_idx)

#         return sorted(list(set(page_indices)))  # Remove duplicates and sort


class SplitPdfStrategy(PdfStrategy):
    """PDF split strategy."""

    async def execute(
        self,
        input_file: Path,
        output_dir: Path,
        pages: str = None,
        **kwargs
    ) -> Path:
        """Split PDF.
        
        Args:
            input_file: Path to input PDF
            output_dir: Directory for output PDFs
            pages: Page ranges (e.g., "1-3,5,7-9" or "all")
            **kwargs: Additional options including 'split_mode'
            
        Returns:
            Path to output directory
            
        Raises:
            ConversionError: If split fails
        """
        try:
            if not input_file.exists():
                raise ConversionError("Input PDF file not found")

            output_dir.mkdir(parents=True, exist_ok=True)

            # Extract split_mode safely (it might be an Enum or a string)
            split_mode = kwargs.get("split_mode", "specific")
            if hasattr(split_mode, "value"):
                split_mode = split_mode.value

            pdf_reader = PdfReader(input_file)
            # 1. Automatically detect the number of pages
            total_pages = len(pdf_reader.pages)

            # 2. Parse page ranges using the new logic
            page_indices = self._parse_page_ranges(pages, total_pages, split_mode)

            if not page_indices:
                raise ConversionError(f"No valid pages specified for extraction in '{split_mode}' mode.")

            # Create a single writer to combine the extracted pages into ONE new PDF
            pdf_writer = PdfWriter()
            for page_idx in page_indices:
                pdf_writer.add_page(pdf_reader.pages[page_idx])

            output_file = output_dir / f"extracted_{split_mode}.pdf"
            with open(output_file, "wb") as f:
                pdf_writer.write(f)

            logger.info(f"PDF split successful: {len(page_indices)} pages extracted into {output_file.name}")
            return output_dir
        except Exception as e:
            logger.error(f"PDF split failed: {str(e)}")
            raise ConversionError(f"Failed to split PDF: {str(e)}")

    def _parse_page_ranges(self, pages: str, total_pages: int, split_mode: str = "specific") -> list:
        """Parse page range string based on the chosen split mode.
        
        Args:
            pages: Page range string (e.g., "1-3,5", "all")
            total_pages: Total number of pages automatically detected
            split_mode: "range", "specific", "even", or "odd"
            
        Returns:
            List of page indices (0-based)
        """
        page_indices = []

        # Handle automatic Even/Odd extraction (ignores 'pages' input)
        if split_mode == "even":
            # Pages 2, 4, 6 -> Indices 1, 3, 5
            return [i for i in range(total_pages) if (i + 1) % 2 == 0]
            
        elif split_mode == "odd":
            # Pages 1, 3, 5 -> Indices 0, 2, 4
            return [i for i in range(total_pages) if (i + 1) % 2 != 0]

        # Handle 'all' or empty fallback
        if not pages or pages.lower() == "all":
            return list(range(total_pages))

        parts = pages.split(",")

        # Handle Range and Specific string parsing
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            if "-" in part:
                try:
                    start, end = part.split("-")
                    start = max(1, int(start.strip())) - 1  # 0-based index
                    end = min(total_pages, int(end.strip()))  # Keep inclusive
                    if start <= end:
                        page_indices.extend(range(start, end))
                except ValueError:
                    continue
            else:
                try:
                    page_idx = int(part) - 1  # 0-based index
                    if 0 <= page_idx < total_pages:
                        page_indices.append(page_idx)
                except ValueError:
                    continue

        return sorted(list(set(page_indices)))  # Remove duplicates and sort sequentially
    

class ImagesToPdfStrategy(PdfStrategy):
    """Images to PDF conversion strategy."""

    async def execute(
        self, input_files: List[Path], output_file: Path, **kwargs
    ) -> Path:
        """Convert images to PDF.
        
        Args:
            input_files: List of paths to image files
            output_file: Path to output PDF
            **kwargs: Additional options (e.g., 'orientation', 'size')
            
        Returns:
            Path to output PDF file
            
        Raises:
            ConversionError: If conversion fails
        """
        try:
            if not input_files:
                raise ConversionError("No image files provided")

            # Convert images and prepare for PDF
            images = []
            for img_file in sorted(input_files):
                if not img_file.exists():
                    raise ConversionError(f"Image file not found: {img_file}")

                try:
                    img = Image.open(img_file)

                    # Convert to RGB if necessary
                    if img.mode in ("RGBA", "LA", "P"):
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        if img.mode == "P":
                            img = img.convert("RGBA")
                        background.paste(
                            img,
                            mask=img.split()[-1] if "A" in img.mode else None
                        )
                        img = background
                    elif img.mode != "RGB":
                        img = img.convert("RGB")

                    images.append(img)
                except Exception as e:
                    logger.warning(f"Failed to process image {img_file}: {str(e)}")
                    raise ConversionError(f"Failed to process image: {str(e)}")

            if not images:
                raise ConversionError("No valid images to convert")

            # Convert to PDF
            try:
                # Use img2pdf for better quality
                img_bytes_list = []
                for img in images:
                    img_bytes = img.tobytes(encoder_name="raw")
                    img_bytes_list.append(img_bytes)

                # Alternative: Use PIL's built-in PDF support
                images[0].save(
                    output_file,
                    save_all=True,
                    append_images=images[1:] if len(images) > 1 else [],
                    format="PDF"
                )
            except Exception as e:
                raise ConversionError(f"Failed to create PDF: {str(e)}")

            logger.info(f"Images to PDF conversion successful: {len(images)} images converted")
            return output_file
        except Exception as e:
            logger.error(f"Images to PDF conversion failed: {str(e)}")
            raise ConversionError(f"Failed to convert images to PDF: {str(e)}")

