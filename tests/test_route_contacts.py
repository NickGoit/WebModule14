from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime

import pytest

from src.database.models import Contact, User
from src.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


def test_create_contact(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.post("/api/contacts/",
                               json={
                                   "first_name": "Tom",
                                   "last_name": "Soyer",
                                   "email": "Tomas@example.com",
                                   "phone": "+31462454652",
                                   "date_of_birth": "2018-04-30"
                               },
                               headers={"Authorization": f"Bearer {token}"}
                               )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["first_name"] == "Tom"
        assert "id" in data


def test_get_contact_by_name(client, token, monkeypatch):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get("/api/contacts/",
                              headers={"Authorization": f"Bearer {token}"}
                              )
        assert response.status_code == 200, response.text


def test_get_contact_by_id(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get("/api/contacts/1",
                              headers={"Authorization": f"Bearer {token}"}
                              )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["first_name"] == "Tom"


def test_get_birthday(client, token):
    with patch.object(auth_service, 'r') as r_mock:
        r_mock.get.return_value = None
        response = client.get("/api/contacts/birthday",
                              headers={"Authorization": f"Bearer {token}"}
                              )
        assert response.status_code == 200, response.text


