from fastapi import APIRouter


router = APIRouter(tags=["health", "slo"])


@router.get("/health", summary="Health check")
async def health() -> dict:
        return {"status": "ok",
            "version": "v1",
            "message": "Everything is working fine"
    }
