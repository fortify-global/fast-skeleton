from app.model.health_model import HealthResponse
from app.model.health_model import get_db_health


class HealthController:

    @classmethod
    async def get_health(cls) -> HealthResponse:  
        db = await get_db_health()
        status = "ok" if db.ok else "degraded"
        message = "Everything is working fine" if db.ok else "Database degraded"
        
        return HealthResponse(status=status, version="v1", message=message)

    @classmethod
    async def get_health_v2(cls) -> HealthResponse:  
        db = await get_db_health()
        status = "ok" if db.ok else "degraded"
        message = "Everything is working fine" if db.ok else "Database degraded"
        
        return HealthResponse(status=status, version="v2", message=message)
    