import pytest
from httpx import AsyncClient
from app.database import get_async_db
from app.main import app
from app.models.user_model import User
from app.utils.security import hash_password

# Example of a test function using the async_client fixture
@pytest.mark.asyncio
async def test_create_user(async_client):
    # Authenticate and get a token
    form_data = {"username": "admin", "password": "secret"}
    token_response = await async_client.post("/token", data=form_data)
    assert token_response.status_code == 200, "Authentication failed"
    access_token = token_response.json().get("access_token")
    assert access_token, "No access token provided"
    headers = {"Authorization": f"Bearer {access_token}"}

    # Data for creating a new user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!"
    }
    response = await async_client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 201, f"Failed to create user: {response.text}"

@pytest.mark.asyncio
async def test_create_user2(async_client):
    # Repeating the login process for a fresh token
    form_data = {"username": "admin", "password": "secret"}
    token_response = await async_client.post("/token", data=form_data)
    assert token_response.status_code == 200
    access_token = token_response.json().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}

    # Attempt to create two users where the second should fail
    user_data1 = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!"
    }
    response1 = await async_client.post("/users/", json=user_data1, headers=headers)
    assert response1.status_code == 201, "First user should be created successfully"

    user_data2 = {
        "username": "testuser3",
        "email": "test@example.com",
        "password": "sS#fdasrongPassword123!"
    }
    response2 = await async_client.post("/users/", json=user_data2, headers=headers)
    assert response2.status_code == 400, "Expected failure on creating second user with duplicate details"


@pytest.mark.asyncio
async def test_retrieve_user(async_client, user, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.get(f"/users/{user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json().get("id") == str(user.id)

@pytest.mark.asyncio
async def test_update_user(async_client, user, token):
    updated_data = {"email": f"updated_{user.id}@example.com"}
    headers = {"Authorization": f"Bearer {token}"}
    response = await async_client.put(f"/users/{user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json().get("email") == updated_data["email"]

@pytest.mark.asyncio
async def test_delete_user(async_client, user, token):
    headers = {"Authorization": f"Bearer {token}"}
    delete_response = await async_client.delete(f"/users/{user.id}", headers=headers)
    assert delete_response.status_code == 204
    fetch_response = await async_client.get(f"/users/{user.id}", headers=headers)
    assert fetch_response.status_code == 404


@pytest.mark.asyncio
async def test_login_success(async_client, user):
    # Set up the test client for FastAPI application

    # Attempt to login with the test user
    response = await async_client.post("/login/", json={"username": user.username, "password": "MySuperPassword$1234"})
    
    # Check for successful login response
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
async def test_delete_user_does_not_exist(async_client, token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"  # Valid UUID format
    headers = {"Authorization": f"Bearer {token}"}
    delete_response = await async_client.delete(f"/users/{non_existent_user_id}", headers=headers)
    assert delete_response.status_code == 404
