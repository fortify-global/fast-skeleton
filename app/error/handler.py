import traceback
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app import logger
from app.error.exception import AppException
from app.error.model import AppExceptionModel
from app.error.message import em


def _traceback_details() -> str:
    return "".join(traceback.format_exc())


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException): 
        exc_response = AppExceptionModel(code=exc.code, key=exc.key, message=exc.message, reason=exc.reason, detail = exc.detail)
        return JSONResponse(status_code=exc.code, content=exc_response.model_dump())

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException): 
        error_key = 'unhandled_exception'
        # [NOTE] You can/should remove details from response after the app is stable
        exc_response = AppExceptionModel(code=exc.status_code, key=error_key, message=em[error_key], detail = exc.detail)
        return JSONResponse(status_code=exc.status_code, content=exc_response.model_dump())

