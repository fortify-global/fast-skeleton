from typing import Any, Optional

from pydantic import BaseModel


class AppExceptionModel(BaseModel):
    code: str
    key: str
    message: str
    reason: str
    detail: Optional[Any] = None
    
