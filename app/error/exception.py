from __future__ import annotations

from app.util.global_values import get_main_error
from typing import Any, Optional

from fastapi import HTTPException
from app.error.message import am, dm

"""
Please provide 
code - generally http code
key - error key - associated message will be fetched from message.py, default key is defualt, avoid defualt
message - 
reson - error exact field,more ecplation about error if can be passed
detail - kind of stack trace , dynamic errors

"""
class AppException(HTTPException):
    def __init__(self, code: int, key: str = 'default', reason: Optional[str] = '', detail: Optional[Any] = None) -> None:
        super().__init__(status_code=code, detail=reason)
        self.code = code
        self.key = key
        self.message = am[key]
        self.reason = reason
        self.detail = get_main_error()

class DatabaseException(AppException):
    def __init__(self, code: int, key:str= 'default', reason: Optional[str] = '', detail: Optional[Any] = None) -> None:
        super().__init__(code=code, reason=reason)
        self.code = code
        self.key = key
        self.message = dm[key]
        self.reason = reason
        self.detail = get_main_error()
        
"""



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
