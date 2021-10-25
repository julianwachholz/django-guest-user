import pytest
from guest_user.functions import is_guest_user


@pytest.mark.django_db
def test_convert_view_with_anonymous(client):
    response = client.get("/convert/")
    assert response.status_code == 302
    assert response.url == "/accounts/login/"


@pytest.mark.django_db
def test_convert_view_with_authenticated(authenticated_client):
    response = authenticated_client.get("/convert/")
    assert response.status_code == 302
    assert response.url == "/accounts/profile/"


@pytest.mark.django_db
def test_convert_view_with_guest(client):
    response = client.get("/allow_guest_user/")
    assert response.status_code == 200
    guest_user = response.context["user"]
    assert is_guest_user(guest_user)

    response = client.post(
        "/convert/",
        {
            "username": "converted_user",
            "password1": "c0mpl3xhunter2",
            "password2": "c0mpl3xhunter2",
        },
    )
    assert response.status_code == 302
    assert response.url == "/convert/success/"

    # Check that the user is now a regular user
    response = client.get("/convert/success/")
    assert response.status_code == 200
    converted_user = response.context["user"]
    assert guest_user.id == converted_user.id
    assert not is_guest_user(converted_user)
