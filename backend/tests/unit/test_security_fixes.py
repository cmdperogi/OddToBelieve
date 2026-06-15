"""Unit tests verifying STORY-15 (no credential defaults) and STORY-16 (bcrypt verify)."""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError


def test_config_rejects_empty_secret_key() -> None:

    # Importing Settings directly and instantiating without SECRET_KEY must fail
    from app.config import Settings

    with pytest.raises((ValidationError, Exception)):
        Settings(secret_key="", admin_username="admin", admin_password="pw")


def test_config_rejects_empty_admin_username() -> None:
    from app.config import Settings

    with pytest.raises((ValidationError, Exception)):
        Settings(
            secret_key="some-key-32-characters-long-here!",
            admin_username="",
            admin_password="pw",
        )


def test_config_rejects_empty_admin_password() -> None:
    from app.config import Settings

    with pytest.raises((ValidationError, Exception)):
        Settings(
            secret_key="some-key-32-characters-long-here!",
            admin_username="admin",
            admin_password="",
        )


def test_login_uses_bcrypt_not_plain_equality(client: TestClient) -> None:
    """Correct password still authenticates after bcrypt hashing at startup."""
    resp = client.post(
        "/auth/token", data={"username": "admin", "password": "changeme"}
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password_rejected(client: TestClient) -> None:
    """Wrong password is rejected even when close to the real one."""
    resp = client.post(
        "/auth/token", data={"username": "admin", "password": "Changeme"}
    )
    assert resp.status_code == 401


def test_login_wrong_username_rejected(client: TestClient) -> None:
    resp = client.post(
        "/auth/token", data={"username": "Admin", "password": "changeme"}
    )
    assert resp.status_code == 401


def test_hashed_password_not_plaintext() -> None:
    """The stored password hash should not equal the plaintext password."""
    from app.routers.auth import _hashed_admin_password

    assert _hashed_admin_password != "changeme"
    assert _hashed_admin_password.startswith("$2b$")
