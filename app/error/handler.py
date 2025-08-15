from app.config.app_setting import Setting
from typing import Any
import json

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app import logger
from app.error.exception import AppException, DatabaseException
from app.error.model import AppExceptionModel, DatabaseExceptionModel
from app.error.message import am
from app.util.global_values import get_complete_traceback


def filter_sensitive_data(data: Any) -> Any:
    """Recursively filter out sensitive fields from data"""
    if isinstance(data, dict):
        filtered = {}
        for key, value in data.items():
            key_lower = key.lower()
            # Filter out sensitive keys
            if any(sensitive in key_lower for sensitive in Setting.SENSITIVE_PATTERNS ):
                filtered[key] = "******"
            else:
                filtered[key] = filter_sensitive_data(value)
        return filtered
    elif isinstance(data, list):
        return [filter_sensitive_data(item) for item in data]
    else:
        return data

def filter_headers(headers: dict) -> dict:
    """Filter out sensitive headers"""
    
    filtered = {}
    for key, value in headers.items():
        if key.lower() in Setting.SENSITIVE_PATTERNS:
            filtered[key] = "********"
        else:
            filtered[key] = value
    return filtered


async def log_exception_details(request: Request, exc_response: AppExceptionModel):
    """Log request details safely, filtering sensitive data"""
    try:
        # Get and filter request body
        body = None
        try:
            body_bytes = await request.body()
            if body_bytes:
                body_str = body_bytes.decode('utf-8')
                # Try to parse JSON and filter sensitive fields
                try:
                    body_data = json.loads(body_str)
                    body = json.dumps(filter_sensitive_data(body_data), indent=2)
                except json.JSONDecodeError:
                    # If not JSON, just filter common patterns
                    body = body_str
                    for sensitive in Setting.SENSITIVE_PATTERNS:
                        body = body.replace(sensitive, '********')
        except Exception:
            body = "Unable to read body"
    
        # Filter sensitive headers
        safe_headers = filter_headers(dict(request.headers))
        
        # Log safely filtered request details
        logger.error(
        f"Error Log | "
        f"Method: {request.method} | "
        f"URL: {request.url} | "
        f"Path: {request.url.path} | "
        f"Query: {dict(request.query_params)} | "
        f"Headers: {safe_headers} | "
        f"Body: {body} | "
        f"Exception: {exc_response}")
    
    except Exception as log_error:
        logger.error(f"Failed to log request details: {log_error}")

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException): 
        exc_response = AppExceptionModel(code=exc.code, key=exc.key, message=exc.message, reason=exc.reason, detail = exc.detail)
        logger.debug(f"Request - {request}\nTraceback = {get_complete_traceback()}\nException - {exc_response}")
        return JSONResponse(status_code=exc.code, content=exc_response.model_dump())

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException): 
        exc_response = DatabaseExceptionModel(code=exc.code, key=exc.key, message=exc.message, reason=exc.reason, detail = exc.detail)
        logger.debug(f"Request - {request}\nTraceback = {get_complete_traceback()}\nException - {exc_response}")
        return JSONResponse(status_code=exc.code, content=exc_response.model_dump())

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException): 
        error_key = 'unhandled_exception'
        # [NOTE] You can/should remove details from response after the app is stable
        exc_response = AppExceptionModel(code=exc.status_code, key=error_key, message=am[error_key], detail = exc.detail)
        logger.debug(f"Request - {request}\n Traceback = {get_complete_traceback()}\n Exception - {exc_response}")
        return JSONResponse(status_code=exc.status_code, content=exc_response.model_dump())
