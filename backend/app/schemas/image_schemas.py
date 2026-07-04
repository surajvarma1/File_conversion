# """Pydantic schemas for image endpoints."""

# from pathlib import Path
# from typing import Optional

# from pydantic import BaseModel, Field, FilePath, validator

# from app.core.config import get_settings

# settings = get_settings()


# class ImageConversionSchema(BaseModel):
#     """Base image conversion schema."""

#     quality: Optional[int] = Field(None, ge=1, le=100, description="Compression quality from 1 to 100")
#     width: Optional[int] = Field(None, gt=0, description="Target width in pixels")
#     height: Optional[int] = Field(None, gt=0, description="Target height in pixels")
#     maintain_aspect: bool = Field(True, description="Maintain original aspect ratio")

#     @validator("quality")
#     def validate_quality(cls, value: Optional[int]) -> Optional[int]:
#         if value is not None and (value < 1 or value > 100):
#             raise ValueError("Quality must be between 1 and 100")
#         return value


# class  ImageResizeSchema(BaseModel):
#     """Schema for image resize."""

#     width: int = Field(..., gt=0, description="Target width in pixels")
#     height: int = Field(..., gt=0, description="Target height in pixels")
#     maintain_aspect: bool = Field(True, description="Maintain original aspect ratio")


# class ImageCompressSchema(BaseModel):
#     """Schema for image compression."""

#     quality: Optional[int] = Field(75, ge=1, le=100, description="Compression quality")
#     max_size: Optional[int] = Field(None, gt=0, description="Maximum output file size in bytes")


# class FileUploadSchema(BaseModel):
#     """Schema for uploaded file metadata."""

#     filename: str
#     mime_type: str
#     size: int

#     @validator("size")
#     def validate_file_size(cls, value: int) -> int:
#         if value > settings.MAX_UPLOAD_SIZE:
#             raise ValueError(f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE} bytes")
#         return value


"""Pydantic schemas for image endpoints."""

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, model_validator, validator

from app.core.config import get_settings

settings = get_settings()

class ResizeMode(str, Enum):
    BY_SIZE = "by_size"
    PERCENTAGE = "percentage"
    SOCIAL_MEDIA = "social_media"

class OutputFormat(str, Enum):
    ORIGINAL = "original"
    JPG = "jpg"
    PNG = "png"
    WEBP = "webp"

class ImageConversionSchema(BaseModel):
    """Base image conversion schema."""
    quality: Optional[int] = Field(None, ge=1, le=100, description="Compression quality from 1 to 100")
    width: Optional[int] = Field(None, gt=0, description="Target width in pixels")
    height: Optional[int] = Field(None, gt=0, description="Target height in pixels")
    maintain_aspect: bool = Field(True, description="Maintain original aspect ratio")

    @validator("quality")
    def validate_quality(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and (value < 1 or value > 100):
            raise ValueError("Quality must be between 1 and 100")
        return value

class ImageResizeSchema(BaseModel):
    """Advanced schema for image resize."""
    resize_mode: ResizeMode = Field(default=ResizeMode.BY_SIZE, description="Mode of resizing")
    
    # Mode: By Size
    width: Optional[int] = Field(None, gt=0, description="Target width in pixels")
    height: Optional[int] = Field(None, gt=0, description="Target height in pixels")
    maintain_aspect: bool = Field(True, description="Maintain original aspect ratio")
    
    # Mode: Percentage
    percentage: Optional[int] = Field(None, gt=0, description="Scale percentage (e.g., 50 for half size)")
    
    # Mode: Social Media
    social_media_preset: Optional[str] = Field(None, description="Preset name (e.g., 'instagram_square', 'twitter_header')")
    
    # Export Settings
    target_size_kb: Optional[int] = Field(None, gt=0, description="Target max file size in KB (JPG only)")
    output_format: OutputFormat = Field(default=OutputFormat.ORIGINAL, description="Target output format")

    @model_validator(mode='after')
    def validate_resize_inputs(self) -> 'ImageResizeSchema':
        """Ensure the correct fields are provided based on the resize_mode."""
        if self.resize_mode == ResizeMode.BY_SIZE:
            if not self.width and not self.height:
                raise ValueError("At least width or height must be provided for 'by_size' mode.")
        elif self.resize_mode == ResizeMode.PERCENTAGE:
            if not self.percentage:
                raise ValueError("Percentage value must be provided for 'percentage' mode.")
        elif self.resize_mode == ResizeMode.SOCIAL_MEDIA:
            if not self.social_media_preset:
                raise ValueError("Social media preset must be provided for 'social_media' mode.")
        return self

class ImageCompressSchema(BaseModel):
    """Schema for image compression."""
    quality: Optional[int] = Field(75, ge=1, le=100, description="Compression quality")
    max_size: Optional[int] = Field(None, gt=0, description="Maximum output file size in bytes")

class FileUploadSchema(BaseModel):
    """Schema for uploaded file metadata."""
    filename: str
    mime_type: str
    size: int

    @validator("size")
    def validate_file_size(cls, value: int) -> int:
        if value > settings.MAX_UPLOAD_SIZE:
            raise ValueError(f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE} bytes")
        return value