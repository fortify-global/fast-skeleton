from fastapi import FastAPI
from app.config.app_config import Config
from app.api.router import api_router_v1, api_router_v2
from app.error.handler import register_exception_handlers

# [TODO] Replace this with your short app name. This will be used million times. 
a_i = FastAPI(title=Config.APP_NAME)
register_exception_handlers(a_i)


a_i.include_router(api_router_v1)
a_i.include_router(api_router_v2)

@a_i.get("/")
async def root():
    return {"message": "Welcome to fast-skeleton"}
