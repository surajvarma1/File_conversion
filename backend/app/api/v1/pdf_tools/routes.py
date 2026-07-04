"""PDF tool API routes."""

import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.application.services import PdfService
from app.core.config import get_settings
from app.core.logging import get_logger
from app.core.security import FileValidator
from app.infrastructure.file_storage import LocalFileStorage
from app.schemas.pdf_schemas import PdfMergeSchema, PdfSplitSchema, ImagesToPdfSchema

logger = get_logger(__name__)
settings = get_settings()
router = APIRouter(prefix="/pdf", tags=["pdf"])


def get_services() -> PdfService:
    file_storage = LocalFileStorage(settings)
    validator = FileValidator(settings)
    return PdfService(settings=settings, file_storage=file_storage, validator=validator)


def _save_upload(file: UploadFile, upload_dir: Path) -> Path:
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination = upload_dir / file.filename
    with destination.open("wb") as buffer:
        while content := file.file.read(8192):
            buffer.write(content)
    return destination


@router.post("/merge", response_model=dict)
async def merge_pdf(
    files: List[UploadFile] = File(...),
    service: PdfService = Depends(get_services),
):
    try:
        if len(files) < 2:
            raise HTTPException(status_code=400, detail="At least two PDF files are required")

        saved_files = []
        for upload_file in files:
            saved_files.append(_save_upload(upload_file, settings.UPLOAD_DIR))

        output_path = settings.OUTPUT_DIR / f"merged_{uuid.uuid4().hex}.pdf"
        await service.merge_pdf(saved_files, output_path)
        storage = LocalFileStorage(settings)
        presigned = storage.generate_presigned_url(output_path.name)
        return {"success": True, "output_file": output_path.name, "download_url": presigned}
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))


# @router.post("/split", response_model=dict)
# async def split_pdf(
#     file: UploadFile = File(...),
#     payload: PdfSplitSchema = Depends(),
#     service: PdfService = Depends(get_services),
# ):
#     try:
#         uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
#         output_dir = settings.OUTPUT_DIR / f"split_{uploaded_path.stem}_{uuid.uuid4().hex}"
#         result_dir = await service.split_pdf(uploaded_path, output_dir, pages=payload.pages)
#         return {"success": True, "output_directory": str(result_dir)}
#     except Exception as exc:
#         logger.error(str(exc))
#         raise HTTPException(status_code=400, detail=str(exc))

# @router.post("/split", response_model=dict)
# async def split_pdf(
#     file: UploadFile = File(...),
#     payload: PdfSplitSchema = Depends(),
#     service: PdfService = Depends(get_services),
# ):
#     try:
#         uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
#         output_dir = settings.OUTPUT_DIR / f"split_{uploaded_path.stem}_{uuid.uuid4().hex}"
        
#         # We pass split_mode into the existing method signature
#         result_dir = await service.split_pdf(
#             input_file=uploaded_path, 
#             output_dir=output_dir, 
#             pages=payload.pages,
#             split_mode=payload.split_mode
#         )
        
#         return {
#             "success": True, 
#             "output_directory": str(result_dir),
#             "split_mode_used": payload.split_mode.value
#         }
#     except Exception as exc:
#         logger.error(str(exc))
#         raise HTTPException(status_code=400, detail=str(exc))
@router.post("/split", response_model=dict)
async def split_pdf(
    file: UploadFile = File(...),
    payload: PdfSplitSchema = Depends(),
    service: PdfService = Depends(get_services),
):
    try:
        uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
        
        # 1. Define a single PDF file path instead of a directory
        output_file_name = f"split_{uploaded_path.stem}_{uuid.uuid4().hex}.pdf"
        output_file_path = settings.OUTPUT_DIR / output_file_name
        
        # 2. Pass the output_file_path to the service
        await service.split_pdf(
            input_file=uploaded_path, 
            output_file=output_file_path, 
            pages=payload.pages,
            split_mode=payload.split_mode
        )
        
        # 3. Generate the download URL for the single file
        storage = LocalFileStorage(settings)
        presigned = storage.generate_presigned_url(output_file_name)
        
        return {
            "success": True, 
            "output_file": output_file_name,
            "download_url": presigned,
            "split_mode_used": payload.split_mode.value
        }
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/images-to-pdf", response_model=dict)
async def images_to_pdf(
    files: List[UploadFile] = File(...),
    service: PdfService = Depends(get_services),
):
    try:
        if not files:
            raise HTTPException(status_code=400, detail="At least one image file is required")

        saved_files = []
        for upload_file in files:
            saved_files.append(_save_upload(upload_file, settings.UPLOAD_DIR))

        output_path = settings.OUTPUT_DIR / f"images_{uuid.uuid4().hex}.pdf"
        await service.images_to_pdf(saved_files, output_path)
        return {"success": True, "output_file": str(output_path)}
    except HTTPException:
        raise
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/download/{filename}")
async def download_file(filename: str):
    storage = LocalFileStorage(settings)
    file_path = settings.OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    presigned = storage.generate_presigned_url(filename)
    return {"url": presigned}
