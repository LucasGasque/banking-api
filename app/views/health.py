from fastapi import APIRouter

health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("/live")
async def live() -> str:
    return "ok"


@health_router.get("/ready")
async def ready() -> str:
    return "ok"
