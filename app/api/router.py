from fastapi import APIRouter

from app.api.v1 import health as health_v1
from app.api.v2 import health as health_v2

api_router_v1 = APIRouter(prefix="/api/v1")
api_router_v2 = APIRouter(prefix="/api/v2")

#[NOTE] Just change this for changing version, you can always include both version
api_router_v1.include_router(health_v1.router)
api_router_v2.include_router(health_v2.router)

