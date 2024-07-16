from datetime import timezone
from httpx import Response
from fastapi import status
import pytest
from faker import Faker

from src.core.todos.schemas import TodoAddSchema


async def test_not_authorized(ac):
    response: Response = await ac.get("/api/v1/todos")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_empty_todos_list(authenticated_ac):
    response: Response = await authenticated_ac.get("/api/v1/todos")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == []


async def test_post_todo(authenticated_ac):
    faker = Faker()
    todo = TodoAddSchema(
        title=faker.first_name(),
        description=faker.text(),
        target_date=faker.date_time_this_month(
            before_now=False, after_now=True, tzinfo=timezone.utc
        ),
    )
    body = todo.model_dump(mode="json")

    response: Response = await authenticated_ac.post("/api/v1/todos", json=body)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["data"]["title"] == todo.title


async def test_post_todo_invalid_body(authenticated_ac):
    faker = Faker()
    todo = TodoAddSchema(
        title=faker.first_name(),
        description=faker.text(),
        target_date=faker.date_time_this_month(
            before_now=False, after_now=True, tzinfo=timezone.utc
        ),
    )
    body = todo.model_dump(mode="json")
    body = {**body, "title": None}

    response: Response = await authenticated_ac.post("/api/v1/todos", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "count_to_add, expected_count",
    [
        (1, 1),
        (5, 5),
    ],
)
async def test_get_todos_list(authenticated_ac, count_to_add, expected_count):
    faker = Faker()
    for _ in range(count_to_add):
        todo = TodoAddSchema(
            title=faker.first_name(),
            description=faker.text(),
            target_date=faker.date_time_this_month(
                before_now=False, after_now=True, tzinfo=timezone.utc
            ),
        )
        body = todo.model_dump(mode="json")

        await authenticated_ac.post("/api/v1/todos", json=body)

    response: Response = await authenticated_ac.get("/api/v1/todos")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected_count


async def test_get_todo_by_id(authenticated_ac):
    response: Response = await authenticated_ac.get("api/v1/todos/11")

    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_todo(authenticated_ac):
    faker = Faker()
    todo = TodoAddSchema(
        title=faker.first_name(),
        description=faker.text(),
        target_date=faker.date_time_this_month(
            before_now=False, after_now=True, tzinfo=timezone.utc
        ),
    )
    body = todo.model_dump(mode="json")

    response: Response = await authenticated_ac.post("/api/v1/todos", json=body)
    todo_id = response.json()["data"]["id"]

    response: Response = await authenticated_ac.delete(f"/api/v1/todos/{todo_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
