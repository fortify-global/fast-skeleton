from fastapi import APIRouter
from app.controller.health_controller import HealthController
from app.model.health_model import HealthResponse

router = APIRouter(tags=["health", "slo"])

@router.get("/health", summary="Health check", response_model=HealthResponse)
async def health() -> HealthResponse:
    return await HealthController.get_health()

