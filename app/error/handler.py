import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app import logger
from app.error.exception import AppException, DatabaseException
from app.error.model import AppExceptionModel, DatabaseExceptionModel
from app.error.message import am
from app.util.global_values import get_complete_traceback
from app.util.global_values import filter_sensitive_data


async def log_exception_details(request: Request, exc_response: AppExceptionModel):
    """Log request details safely, filtering sensitive data"""
    try:
        body = None
        try:
            body_bytes = await request.body()
            if body_bytes:
                body_str = body_bytes.decode('utf-8')
                try:
                    body_data = json.loads(body_str)
                    body = json.dumps(filter_sensitive_data(body_data), indent=2)
                except json.JSONDecodeError:
                    body = body_str
                    
        except Exception:
            body = "Unable to read body"
    
        safe_headers = filter_sensitive_data(dict(request.headers))
        
        logger.error(
        f"Exception Error Log \n"
        f"Method: {request.method} | "
        f"URL: {request.url} | "
        f"Path: {request.url.path} | "
        f"Query: {dict(request.query_params)} | "
        f"Headers: {safe_headers} | "
        f"Body: {body} \n"
        f"Exception: {exc_response}")
    
    except Exception as log_error:
        logger.error(f"Failed to log request details: {log_error}")

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException): 
        exc_response = AppExceptionModel(code=exc.code, key=exc.key, message=exc.message, reason=exc.reason, detail = exc.detail)
        await log_exception_details(request, exc_response)
        return JSONResponse(status_code=exc.code, content=exc_response.model_dump())

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException): 
        exc_response = DatabaseExceptionModel(code=exc.code, key=exc.key, message=exc.message, reason=exc.reason, detail = exc.detail)
        await log_exception_details(request, exc_response)
        return JSONResponse(status_code=exc.code, content=exc_response.model_dump())

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException): 
        error_key = 'unhandled_exception'
        # [NOTE] You can/should remove details from response after the app is stable
        exc_response = AppExceptionModel(code=exc.status_code, key=error_key, message=am[error_key], detail = exc.detail)
        await log_exception_details(request, exc_response)
        return JSONResponse(status_code=exc.status_code, content=exc_response.model_dump())
