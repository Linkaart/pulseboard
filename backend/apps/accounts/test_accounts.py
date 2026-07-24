import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestRegister:
    def test_register_creates_user(self, api_client, company):
        payload = {
            "email": "new@example.com",
            "password": "StrongPass123",
            "first_name": "New",
            "last_name": "User",
            "company": company.id,
        }
        response = api_client.post("/api/auth/register/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="new@example.com").exists()
        user = User.objects.get(email="new@example.com")
        assert user.check_password("StrongPass123")

    def test_register_requires_password_min_length(self, api_client):
        payload = {
            "email": "short@example.com",
            "password": "short",
            "first_name": "Short",
            "last_name": "Pass",
        }
        response = api_client.post("/api/auth/register/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    def test_login_returns_tokens(self, api_client, user):
        response = api_client.post(
            "/api/auth/login/",
            {"username": user.username, "password": "StrongPass123"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials(self, api_client, user):
        response = api_client.post(
            "/api/auth/login/",
            {"username": user.username, "password": "wrongpass"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestMe:
    def test_me_requires_authentication(self, api_client):
        response = api_client.get("/api/auth/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_returns_current_user(self, auth_client, user):
        response = auth_client.get("/api/auth/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email

    def test_me_patch_updates_profile(self, auth_client):
        response = auth_client.patch("/api/auth/me/", {"first_name": "Updated"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Updated"
