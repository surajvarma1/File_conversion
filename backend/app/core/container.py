"""Dependency injection container."""

from dependency_injector import containers, providers
from app.core.config import get_settings
from app.infrastructure.file_storage.local_storage import LocalFileStorage
from app.core.security.validator import FileValidator
from app.application.services.conversion_services import (
    ImageConversionService,
    PdfService,
    ZipService,
)


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(get_settings)

    # Infrastructure
    local_storage = providers.Singleton(LocalFileStorage, settings=config)

    # Security
    file_validator = providers.Singleton(FileValidator, settings=config)

    # Application services
    image_service = providers.Factory(
        ImageConversionService,
        settings=config,
        file_storage=local_storage,
        validator=file_validator,
    )

    pdf_service = providers.Factory(
        PdfService,
        settings=config,
        file_storage=local_storage,
        validator=file_validator,
    )

    zip_service = providers.Factory(
        ZipService,
        settings=config,
        file_storage=local_storage,
        validator=file_validator,
    )
