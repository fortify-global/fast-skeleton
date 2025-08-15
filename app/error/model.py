from typing import Any, Optional

from pydantic import BaseModel


class AppExceptionModel(BaseModel):
    code: int
    key: str
    message: str
    reason: str
    detail: Optional[Any] = None
    

class DatabaseExceptionModel(BaseModel):
    code: int
    key: str
    message: str
    reason: str
    detail: Optional[Any] = None
