"""Image tool API routes."""

import os
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.application.services import ImageConversionService
from app.core.config import get_settings
from app.core.logging import get_logger
from app.core.security import FileValidator
from app.infrastructure.file_storage import LocalFileStorage
from app.schemas.image_schemas import (
    ImageCompressSchema,
    ImageResizeSchema,
    ImageConversionSchema,
)

logger = get_logger(__name__)
settings = get_settings()
router = APIRouter(prefix="/image", tags=["image"])


def get_services() -> ImageConversionService:
    file_storage = LocalFileStorage(settings)
    validator = FileValidator(settings)
    return ImageConversionService(settings=settings, file_storage=file_storage, validator=validator)


def _save_upload(file: UploadFile, upload_dir: Path) -> Path:
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination = upload_dir / file.filename
    with destination.open("wb") as buffer:
        while content := file.file.read(8192):
            buffer.write(content)
    return destination


@router.post("/jpg-to-png", response_model=dict)
async def jpg_to_png(
    file: UploadFile = File(...),
    service: ImageConversionService = Depends(get_services),
):
    try:
        uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
        output_path = settings.OUTPUT_DIR / f"{uploaded_path.stem}.png"
        await service.convert_jpg_to_png(uploaded_path, output_path)
        storage = LocalFileStorage(settings)
        presigned = storage.generate_presigned_url(output_path.name)
        return {"success": True, "output_file": output_path.name, "download_url": presigned}
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/png-to-jpg", response_model=dict)
async def png_to_jpg(
    file: UploadFile = File(...),
    payload: ImageConversionSchema = Depends(),
    service: ImageConversionService = Depends(get_services),
):
    try:
        uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
        output_path = settings.OUTPUT_DIR / f"{uploaded_path.stem}.jpg"
        await service.convert_png_to_jpg(uploaded_path, output_path, quality=payload.quality or 85)
        storage = LocalFileStorage(settings)
        presigned = storage.generate_presigned_url(output_path.name)
        return {"success": True, "output_file": output_path.name, "download_url": presigned}
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/webp-to-jpg", response_model=dict)
async def webp_to_jpg(
    file: UploadFile = File(...),
    payload: ImageConversionSchema = Depends(),
    service: ImageConversionService = Depends(get_services),
):
    try:
        uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
        output_path = settings.OUTPUT_DIR / f"{uploaded_path.stem}.jpg"
        await service.convert_webp_to_jpg(uploaded_path, output_path, quality=payload.quality or 85)
        storage = LocalFileStorage(settings)
        presigned = storage.generate_presigned_url(output_path.name)
        return {"success": True, "output_file": output_path.name, "download_url": presigned}
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/jpg-to-webp", response_model=dict)
async def jpg_to_webp(
    file: UploadFile = File(...),
    payload: ImageConversionSchema = Depends(),
    service: ImageConversionService = Depends(get_services),
):
    try:
        uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
        output_path = settings.OUTPUT_DIR / f"{uploaded_path.stem}.webp"
        await service.convert_jpg_to_webp(uploaded_path, output_path, quality=payload.quality or 80)
        storage = LocalFileStorage(settings)
        presigned = storage.generate_presigned_url(output_path.name)
        return {"success": True, "output_file": output_path.name, "download_url": presigned}
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))


# @router.post("/resize", response_model=dict)
# async def resize_image(
#     file: UploadFile = File(...),
#     payload: ImageResizeSchema = Depends(),
#     service: ImageConversionService = Depends(get_services),
# ):
#     try:
#         uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
#         output_path = settings.OUTPUT_DIR / f"{uploaded_path.stem}_resized{uploaded_path.suffix}"
#         await service.resize_image(
#             uploaded_path,
#             output_path,
#             width=payload.width,
#             height=payload.height,
#             maintain_aspect=payload.maintain_aspect,
#         )
#         storage = LocalFileStorage(settings)
#         presigned = storage.generate_presigned_url(output_path.name)
#         return {"success": True, "output_file": output_path.name, "download_url": presigned}
#     except Exception as exc:
#         logger.error(str(exc))
#         raise HTTPException(status_code=400, detail=str(exc))

@router.post("/resize", response_model=dict)
async def resize_image(
    file: UploadFile = File(...),
    payload: ImageResizeSchema = Depends(),
    service: ImageConversionService = Depends(get_services),
):
    try:
        uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
        
        # Determine target extension based on Export Settings
        ext = uploaded_path.suffix.lower()
        if payload.output_format != "original":
            ext = f".{payload.output_format.value}"
            
        output_path = settings.OUTPUT_DIR / f"{uploaded_path.stem}_resized{ext}"
        
        # Pass the entire payload to the service to handle complex logic
        await service.resize_image(
            input_file=uploaded_path,
            output_file=output_path,
            payload=payload
        )
        
        storage = LocalFileStorage(settings)
        presigned = storage.generate_presigned_url(output_path.name)
        return {"success": True, "output_file": output_path.name, "download_url": presigned}
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/compress", response_model=dict)
async def compress_image(
    file: UploadFile = File(...),
    payload: ImageCompressSchema = Depends(),
    service: ImageConversionService = Depends(get_services),
):
    try:
        uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
        output_path = settings.OUTPUT_DIR / f"{uploaded_path.stem}_compressed{uploaded_path.suffix}"
        await service.compress_image(
            uploaded_path,
            output_path,
            quality=payload.quality or 75,
            max_size=payload.max_size,
        )
        storage = LocalFileStorage(settings)
        presigned = storage.generate_presigned_url(output_path.name)
        return {"success": True, "output_file": output_path.name, "download_url": presigned}
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/download/{filename}")
async def download_file(filename: str):
    # Return a presigned download URL rather than serving directly
    storage = LocalFileStorage(settings)
    # Ensure file exists
    file_path = settings.OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    presigned = storage.generate_presigned_url(filename)
    return {"url": presigned}
