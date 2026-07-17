from httpx import AsyncClient, Response


async def test_register_login_me_logout(ac: AsyncClient, clear_cookies: None):
    email = "vlad@gmail.com"
    password = "123456"
    username = "developer"

    response_register: Response = await ac.post(
        url="/auth/register",
        json={"email": email, "password": password, "username": username},
    )
    assert response_register.status_code == 200
    assert response_register.json() == {"status": "OK"}

    response_login: Response = await ac.post(
        url="/auth/login", json={"email": email, "password": password}
    )
    assert response_login.status_code == 200
    assert ac.cookies["access_token"]

    response_me: Response = await ac.get(url="/auth/me")
    assert response_me.status_code == 200
    user = response_me.json()
    assert isinstance(user, dict)
    assert user["email"] == email
    assert user["username"] == username
    assert "password" not in user
    assert "hashed_password" not in user

    response_logout: Response = await ac.post(url="/auth/logout")
    assert response_logout.status_code == 200
    assert response_logout.json() == {"status": "OK"}
    assert ac.cookies.get(name="access_token") is None

    response_double_me: Response = await ac.get(url="/auth/me")
    assert response_double_me.status_code == 401
