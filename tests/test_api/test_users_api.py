import pytest
from httpx import AsyncClient
from app.database import get_async_db
from app.main import app
from app.models.user_model import User
from app.utils.security import hash_password

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def auth_token(async_client):
    user_credentials = {"username": "admin", "password": "secret"}
    response = await async_client.post("/token", data=user_credentials)
    return response.json()["access_token"]

@pytest.mark.asyncio
async def test_create_user(async_client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!",
    }
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_create_user_duplicate_username(async_client, auth_token, user):
    headers = {"Authorization": f"Bearer {auth_token}"}
    user_data = {
        "username": user.username,
        "email": "unique@example.com",
        "password": "AnotherPassword123!",
    }
    response = await async_client.post("/register/", json=user_data, headers=headers)
    assert response.status_code == 400
    assert "Username already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_retrieve_user(async_client, user, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get(f"/users/{user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == str(user.id)

@pytest.mark.asyncio
async def test_retrieve_user2(async_client, user, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get(f"/users/{user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == str(user.username)

@pytest.mark.asyncio
async def test_update_user(async_client, user, token):
    updated_data = {"email": f"updated_{user.id}@example.com"}
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.put(f"/users/{user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]

@pytest.mark.asyncio
async def test_update_user2(async_client, user, token):
    updated_data = {"email": f"updated_{user.id}@example.com","bio": "I am a senior ."}
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.put(f"/users/{user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == updated_data["email"]
    assert response.json()["bio"] == updated_data["bio"]

@pytest.mark.asyncio
async def test_delete_user(async_client, user, token):
    headers = {"Authorization": f"Bearer {token}"}
    delete_response = await async_client.delete(f"/users/{user.id}", headers=headers)
    assert delete_response.status_code == 204
    # Verify the user is deleted
    fetch_response = await async_client.get(f"/users/{user.id}", headers=headers)
    assert fetch_response.status_code == 404


@pytest.mark.asyncio
async def test_login_success(async_client, user):
    response = await async_client.post("/login/", json={"username": user.username, "password": "MySuperPassword$1234"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_create_user_duplicate_username(async_client, user):
    user_data = {
        "username": user.username,
        "email": "unique@example.com",
        "password": "AnotherPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 400
    assert "Username already exists" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client):
    user_data = {
        "username": "uniqueuser",
        "email": "notanemail",
        "password": "ValidPassword123!",
    }
    response = await async_client.post("/register/", json=user_data)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_login_user_not_found(async_client):
    login_data = {
        "username": "nonexistentuser",
        "password": "DoesNotMatter123!"
    }
    response = await async_client.post("/login/", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_incorrect_password(async_client, user):
    login_data = {
        "username": user.username,
        "password": "IncorrectPassword123!"
    }
    response = await async_client.post("/login/", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json().get("detail", "")
    
@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client, auth_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"
    headers = {"Authorization": f"Bearer {auth_token}"}
    delete_response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert delete_response.status_code == 404

# Additional tests can be refactored in a similar manner...
