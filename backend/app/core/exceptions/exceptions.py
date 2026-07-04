"""Custom application exceptions."""


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 400, error_code: str = "APP_ERROR"):
        """Initialize exception.
        
        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Error code for API response
        """
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class FileValidationError(AppException):
    """File validation error."""

    def __init__(self, message: str):
        super().__init__(message, status_code=422, error_code="FILE_VALIDATION_ERROR")


class ConversionError(AppException):
    """File conversion error."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400, error_code="CONVERSION_ERROR")


class StorageError(AppException):
    """Storage operation error."""

    def __init__(self, message: str):
        super().__init__(message, status_code=500, error_code="STORAGE_ERROR")


class NotFoundError(AppException):
    """Resource not found error."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404, error_code="NOT_FOUND")


class InvalidFormatError(FileValidationError):
    """Invalid file format error."""

    def __init__(self, message: str = "Invalid file format"):
        super().__init__(message)


class FileSizeError(FileValidationError):
    """File size error."""

    def __init__(self, message: str = "File size exceeds maximum limit"):
        super().__init__(message)


class CorruptedFileError(FileValidationError):
    """Corrupted file error."""

    def __init__(self, message: str = "File appears to be corrupted"):
        super().__init__(message)
