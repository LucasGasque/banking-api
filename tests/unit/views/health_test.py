import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_live(app_client: AsyncClient):
    response = await app_client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == "ok"


@pytest.mark.asyncio
async def test_ready(app_client: AsyncClient):
    response = await app_client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json() == "ok"
