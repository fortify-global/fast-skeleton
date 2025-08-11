from fastapi import APIRouter


router = APIRouter(tags=["user"])


@router.get("/user", summary="User check")
async def health() -> dict:
        return {"status": "ok",
            "version": "v1",
            "message": "User exist"
    }
