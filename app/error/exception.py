from __future__ import annotations

from typing import Any, Optional

from fastapi import HTTPException
from app.error.error_message import em


class AppException(HTTPException):
    def __init__(self, code: int, key: str, reason: Optional[str] = '', detail: Optional[Any] = None) -> None:
        super().__init__(reason)
        self.code = code
        self.key = key
        self.message = em.get[key]
        self.reason = reason
        self.detail = detail
        
"""
class DatabaseException(AppException):
    def __init__(self, message: str, *, code: str = "DATABASE_ERROR", key: str = "database_error", details: Optional[Any] = None) -> None:
        super().__init__(message)
        self.code = code
        self.key = key
        self.message = message
        self.details = details


class ThirdPartyError(AppException):
    def __init__(
        self,
        message: str,
        code: str = "THIRD_PARTY_ERROR",
        key: str = "third_party_error",
        details: Optional[Any] = None,
        http_status: int = 502,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.key = key
        self.message = message
        self.details = details
        self.http_status = http_status

"""
"""
# Convenience subclasses for common handlable errors
class AccessDeniedError(AppException):
    def __init__(self, message: str = "Access denied", details: Optional[Any] = None) -> None:
        super().__init__(code="ACCESS_DENIED", key="access_denied", message=message, details=details, http_status=403)


class InvalidRequestError(AppError):
    def __init__(self, message: str = "Invalid request", details: Optional[Any] = None) -> None:
        super().__init__(code="INVALID_REQUEST", key="invalid_request", message=message, details=details, http_status=400)


class NotFoundError(AppError):
    def __init__(self, message: str = "Item not found", details: Optional[Any] = None) -> None:
        super().__init__(code="NOT_FOUND", key="not_found", message=message, details=details, http_status=404)


"""