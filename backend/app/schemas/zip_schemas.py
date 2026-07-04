"""Pydantic schemas for ZIP endpoint."""

from pydantic import BaseModel, Field


class ZipExtractSchema(BaseModel):
    """Schema for ZIP extraction endpoint."""

    file_id: str = Field(..., min_length=1, description="Uploaded ZIP file identifier")
