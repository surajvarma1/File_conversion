"""ZIP tool API routes."""

import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.application.services import ZipService
from app.core.config import get_settings
from app.core.logging import get_logger
from app.core.security import FileValidator
from app.infrastructure.file_storage import LocalFileStorage
from app.schemas.zip_schemas import ZipExtractSchema

logger = get_logger(__name__)
settings = get_settings()
router = APIRouter(prefix="/zip", tags=["zip"])


def get_services() -> ZipService:
    file_storage = LocalFileStorage(settings)
    validator = FileValidator(settings)
    return ZipService(settings=settings, file_storage=file_storage, validator=validator)


def _save_upload(file: UploadFile, upload_dir: Path) -> Path:
    upload_dir.mkdir(parents=True, exist_ok=True)
    destination = upload_dir / file.filename
    with destination.open("wb") as buffer:
        while content := file.file.read(8192):
            buffer.write(content)
    return destination


# @router.post("/extract", response_model=dict)
# async def extract_zip(
#     file: UploadFile = File(...),
#     service: ZipService = Depends(get_services),
# ):
#     try:
#         uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
#         output_dir = settings.OUTPUT_DIR / f"extracted_{uploaded_path.stem}_{uuid.uuid4().hex}"
#         result_dir = await service.extract_zip(uploaded_path, output_dir)
#         return {"success": True, "output_directory": str(result_dir)}
#     except Exception as exc:
#         logger.error(str(exc))
#         raise HTTPException(status_code=400, detail=str(exc))


# @router.get("/download/{filename}")
# async def download_file(filename: str):
#     storage = LocalFileStorage(settings)
#     file_path = settings.OUTPUT_DIR / filename
#     if not file_path.exists():
#         raise HTTPException(status_code=404, detail="File not found")
#     presigned = storage.generate_presigned_url(filename)
#     return {"url": presigned}
import os

@router.post("/extract", response_model=dict)
async def extract_zip(
    file: UploadFile = File(...),
    service: ZipService = Depends(get_services),
):
    try:
        uploaded_path = _save_upload(file, settings.UPLOAD_DIR)
        folder_name = f"extracted_{uploaded_path.stem}_{uuid.uuid4().hex}"
        output_dir = settings.OUTPUT_DIR / folder_name
        
        # Extract the ZIP (Service remains the same)
        result_dir = await service.extract_zip(uploaded_path, output_dir)
        
        # Map out all extracted files so the frontend can display them
        extracted_files = []
        for root, _, files in os.walk(result_dir):
            for f in files:
                full_path = Path(root) / f
                # Get the relative path (e.g., "extracted_123/document.pdf")
                relative_path = full_path.relative_to(settings.OUTPUT_DIR)
                
                # Append to list with a generated download URL
                storage = LocalFileStorage(settings)
                download_url = storage.generate_presigned_url(str(relative_path))
                
                extracted_files.append({
                    "filename": f,
                    "filepath": str(relative_path),
                    "download_url": download_url
                })

        return {
            "success": True, 
            "extracted_folder": folder_name,
            "files": extracted_files
        }
    except Exception as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=400, detail=str(exc))


# IMPORTANT: Change {filename} to {file_path:path} to allow slashes in the URL
# This ensures it can find files inside the "extracted_xyz" directories.
@router.get("/download/{file_path:path}")
async def download_file(file_path: str):
    storage = LocalFileStorage(settings)
    target_path = settings.OUTPUT_DIR / file_path
    
    if not target_path.exists() or not target_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
        
    presigned = storage.generate_presigned_url(file_path)
    return {"url": presigned}