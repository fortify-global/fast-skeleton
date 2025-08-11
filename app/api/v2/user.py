from fastapi import APIRouter


router = APIRouter(tags=["user"])


@router.get("/user", summary="User check", include_in_schema=False)
async def health() -> dict:
        return {"status": "ok",
            "version": "v2",
            "message": "User exist"
    }