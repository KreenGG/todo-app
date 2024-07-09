import pytest
from httpx import AsyncClient, Response


@pytest.mark.asyncio
async def test_get_empty_todo_list(
    ac: AsyncClient,
):
    response: Response = await ac.get("/api/v1/todos")

    assert response.status_code == 200
    assert response.json()["data"] == []
