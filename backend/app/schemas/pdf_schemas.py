"""Pydantic schemas for PDF endpoints."""

from typing import List, Optional

from pydantic import BaseModel, Field


class PdfMergeSchema(BaseModel):
    """Schema for PDF merge endpoint."""

    file_ids: List[str] = Field(..., min_length=2, description="List of file IDs for PDF merge")


# class PdfSplitSchema(BaseModel):
#     """Schema for PDF split endpoint."""

#     pages: Optional[str] = Field(None, description="Page ranges to extract (e.g., '1-3,5')")

"""Schema for PDF endpoints."""

from enum import Enum
from pydantic import BaseModel, Field, model_validator
# from typing import Optional

class SplitMode(str, Enum):
    RANGE = "range"        # Example: "1-5" (From page 1 to 5)
    SPECIFIC = "specific"  # Example: "1,4,5" (Random specific pages together)
    EVEN = "even"          # All even pages
    ODD = "odd"            # All odd pages

class PdfSplitSchema(BaseModel):
    """Schema for PDF split endpoint."""
    split_mode: SplitMode = Field(
        default=SplitMode.SPECIFIC, 
        description="Mode of splitting: range, specific, even, or odd"
    )
    pages: Optional[str] = Field(
        None, 
        description="Page ranges to extract (e.g., '1-5' for range, '1,4,5' for specific). Not required for even/odd."
    )

    @model_validator(mode='after')
    def validate_pages_input(self) -> 'PdfSplitSchema':
        """Ensure 'pages' is provided if the mode requires it."""
        if self.split_mode in (SplitMode.RANGE, SplitMode.SPECIFIC) and not self.pages:
            raise ValueError(f"'pages' parameter must be provided when using '{self.split_mode.value}' mode.")
        return self
class ImagesToPdfSchema(BaseModel):
    """Schema for images to PDF endpoint."""

    file_ids: List[str] = Field(..., min_length=1, description="List of image file IDs to convert to PDF")
