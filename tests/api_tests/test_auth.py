from httpx import AsyncClient, Response
import pytest


async def test_register(
    ac: AsyncClient,
):
    body = {
        "email": "test@test.com",
        "password": "password",
    }
    response: Response = await ac.post("/api/v1/auth/register", json=body)

    assert response.status_code == 201
    assert response.json()["data"]["email"] == "test@test.com"


async def test_register_already_exists(
    ac: AsyncClient,
):
    body = {
        "email": "test@test.com",
        "password": "password",
    }
    await ac.post("/api/v1/auth/register", json=body)
    response: Response = await ac.post("/api/v1/auth/register", json=body)

    assert response.status_code == 409


@pytest.mark.parametrize(
    "email, password",
    [
        ("testtest.com", "password"),
        ("test@test", "password"),
        ("@test.com", "password"),
        ("test@test.com", "sss"),
        ("test@test.com", ""),
        ("", "password"),
    ],
)
async def test_register_invalid_input(
    ac: AsyncClient,
    email,
    password,
):
    body = {
        "email": email,
        "password": password,
    }
    response: Response = await ac.post("/api/v1/auth/register", json=body)

    assert response.status_code == 422


async def test_login(
    ac: AsyncClient,
):
    body = {
        "email": "test@test.com",
        "password": "password",
    }
    await ac.post("/api/v1/auth/register", json=body)
    response: Response = await ac.post("/api/v1/auth/login", json=body)

    assert response.status_code == 200
    assert response.cookies.get("access_token") is not None


@pytest.mark.parametrize(
    "email, password",
    [
        ("testtest.com", "password"),
        ("test@test", "password"),
        ("@test.com", "password"),
        ("test@test.com", "sss"),
        ("test@test.com", ""),
        ("", "password"),
    ],
)
async def test_login_invalid_input(
    ac: AsyncClient,
    email,
    password,
):
    body = {
        "email": email,
        "password": password,
    }
    await ac.post("/api/v1/auth/register", json=body)
    response: Response = await ac.post("/api/v1/auth/login", json=body)

    assert response.status_code == 422


async def test_logout(
    ac: AsyncClient,
):
    body = {
        "email": "test@test.com",
        "password": "password",
    }
    await ac.post("/api/v1/auth/register", json=body)
    response: Response = await ac.post("/api/v1/auth/login", json=body)

    assert response.status_code == 200
    assert response.cookies.get("access_token") is not None

    response: Response = await ac.post("/api/v1/auth/logout", json=body)

    assert response.status_code == 200
    assert response.cookies.get("access_token") is None
