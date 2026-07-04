# File Conversion Platform

A professional file conversion platform built with Next.js and FastAPI. Supports image conversion, image resize/compression, PDF merge/split, images-to-PDF, and ZIP extraction.

## Features

- JPG → PNG
- PNG → JPG
- WebP → JPG
- JPG → WebP
- Image Resize
- Image Compress
- Images → PDF
- PDF Merge
- PDF Split
- ZIP Extractor

## Tech Stack

- Frontend: Next.js 15, TypeScript, Tailwind CSS
- Backend: FastAPI, Python 3.12, Pydantic v2, Dependency Injector
- Image processing: Pillow
- PDF processing: pypdf, img2pdf
- ZIP processing: zipfile, pyzipper

## Installation

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Docker

```bash
docker-compose up --build
```

## API Endpoints

- `POST /api/v1/image/jpg-to-png`
- `POST /api/v1/image/png-to-jpg`
- `POST /api/v1/image/webp-to-jpg`
- `POST /api/v1/image/jpg-to-webp`
- `POST /api/v1/image/resize`
- `POST /api/v1/image/compress`
- `POST /api/v1/pdf/merge`
- `POST /api/v1/pdf/split`
- `POST /api/v1/pdf/images-to-pdf`
- `POST /api/v1/zip/extract`

## Security

- MIME validation
- Magic-byte file signature validation
- File size limiting
- Rate limiting middleware
- Secure temporary file storage

## Notes

This project provides a clean architecture and extensible strategy/factory patterns for conversion tasks. It is designed for production-ready deployment and scalable extension.
