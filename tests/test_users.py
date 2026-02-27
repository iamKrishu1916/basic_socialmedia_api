import pytest
from app import schemas
from jose import jwt
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     print(res.json().get("message"))
#     assert res.json().get("message") == "Welcomoe to my api!"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/user", json={"email": "hello1@gmail.com", "password": "password"}
    )
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert res.json().get("email") == "hello1@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")

    assert res.status_code == 200
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("krishu123@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "outofthebox", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "outofthebox", 422),
        ("krishu123@gmail.com", None, 422),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get("detail") == "INVALID CREDENTIALS"
