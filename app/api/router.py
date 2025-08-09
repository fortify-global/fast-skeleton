from fastapi import APIRouter

from .v1 import health as health_v1


api_router_v1 = APIRouter(prefix="/api/v1")
api_router_v1.include_router(health_v1.router)


