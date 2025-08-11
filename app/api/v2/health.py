from fastapi import APIRouter


router = APIRouter(tags=["health", "slo"])


@router.get("/health", summary="Health check", include_in_schema=False)
async def health() -> dict:
    return {"status": "ok",
            "version": "v2",
            "message": "Everything is working fine"
    }


