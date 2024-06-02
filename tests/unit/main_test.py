import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(app_client: AsyncClient):
    response = await app_client.get("/")
    assert response.status_code == 200
