def test_register_and_login(client):
    email = "newuser@example.com"
    register = client.post(
        "/api/v1/auth/register",
        json={"email": email, "name": "New User", "password": "password123"},
    )
    assert register.status_code == 200
    assert "access_token" in register.json()

    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "password123"},
    )
    assert login.status_code == 200
    assert login.json()["user"]["email"] == email


def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"]["error"]["code"] == "INVALID_CREDENTIALS"