

# """Signed download endpoints."""

# import shutil
# from pathlib import Path
# from typing import Optional

# from fastapi import APIRouter, HTTPException, Query
# from fastapi.responses import FileResponse

# from app.core.config import get_settings
# from app.core.logging import get_logger
# from app.infrastructure.file_storage.local_storage import LocalFileStorage

# settings = get_settings()
# logger = get_logger(__name__)
# router = APIRouter(prefix="/download", tags=["download"])


# @router.get("/serve")
# async def serve_file(filename: str = Query(...), expires: int = Query(...), sig: str = Query(...)):
#     storage = LocalFileStorage(settings)

#     # Validate signature and expiry
#     if not storage.verify_presigned(filename, expires, sig):
#         logger.warning("Invalid or expired presigned download link attempted")
#         raise HTTPException(status_code=403, detail="Invalid or expired download link")

#     file_path = settings.OUTPUT_DIR / filename
    
#     if not file_path.exists():
#         logger.warning(f"Requested download not found: {filename}")
#         raise HTTPException(status_code=404, detail="File not found")

#     # --- THE FIX ---
#     # Check if the requested path is actually a directory (like PDF split or ZIP extract outputs)
#     if file_path.is_dir():
#         logger.info(f"Directory detected. Compressing {file_path} into a zip file...")
        
#         # shutil.make_archive works best with strings, so we convert the Path object
#         zip_path_str = shutil.make_archive(
#             base_name=str(file_path), # Saves it as /outputs/filename.zip
#             format='zip',        
#             root_dir=str(file_path)   # What folder to zip up
#         )
        
#         return FileResponse(
#             path=zip_path_str, 
#             filename=f"{filename}.zip", 
#             media_type="application/zip"
#         )
#     # ---------------

#     # If it's a standard single file, serve it normally
#     return FileResponse(path=file_path, filename=file_path.name)



"""Signed download endpoints."""

import shutil
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse

from app.core.config import get_settings
from app.core.logging import get_logger
from app.infrastructure.file_storage.local_storage import LocalFileStorage

settings = get_settings()
logger = get_logger(__name__)
router = APIRouter(prefix="/download", tags=["download"])


@router.get("/serve")
async def serve_file(filename: str = Query(...), expires: int = Query(...), sig: str = Query(...)):
    storage = LocalFileStorage(settings)

    # Validate signature and expiry
    if not storage.verify_presigned(filename, expires, sig):
        logger.warning("Invalid or expired presigned download link attempted")
        raise HTTPException(status_code=403, detail="Invalid or expired download link")

    file_path = settings.OUTPUT_DIR / filename
    
    if not file_path.exists():
        logger.warning(f"Requested download not found: {filename}")
        raise HTTPException(status_code=404, detail="File not found")

    # --- THE FIX ---
    # Check if the requested path is actually a directory (like PDF split or ZIP extract outputs)
    if file_path.is_dir():
        logger.info(f"Directory detected. Compressing {file_path} into a zip file...")
        
        # shutil.make_archive works best with strings, so we convert the Path object
        zip_path_str = shutil.make_archive(
            base_name=str(file_path), # Saves it as /outputs/filename.zip
            format='zip',        
            root_dir=str(file_path)   # What folder to zip up
        )
        
        return FileResponse(
            path=zip_path_str, 
            filename=f"{filename}.zip", 
            media_type="application/zip"
        )
    # ---------------

    # If it's a standard single file, serve it normally
    return FileResponse(path=file_path, filename=file_path.name)