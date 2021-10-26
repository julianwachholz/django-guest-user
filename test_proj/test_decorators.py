import pytest
from guest_user.functions import is_guest_user

# see views.py for view functions used in these tests


@pytest.mark.django_db
def test_allow_guest_user_with_anonymous(client):
    """
    Unauthenticated visitors get automatically logged in as a guest user.
    """
    response = client.get("/allow_guest_user/")

    assert response.status_code == 200
    response_user = response.context["user"]
    assert not response_user.is_anonymous
    assert len(response_user.username) == 32  # uuid4 length
    assert is_guest_user(response_user)


@pytest.mark.django_db
def test_allow_guest_user_with_authenticated(authenticated_client):
    """
    Authenticated visitors should stay logged in.
    """
    response = authenticated_client.get("/allow_guest_user/")
    assert response.status_code == 200
    response_user = response.context["user"]
    assert not response_user.is_anonymous
    assert response_user.username == "registered_user"
    assert not is_guest_user(response_user)


@pytest.mark.django_db
def test_guest_user_required_with_anonymous(client):
    """
    If a visitor isn't a guest user yet, they should
    be redirected to the login page.

    """
    response = client.get("/guest_user_required/")

    assert response.status_code == 302
    assert response.url == "/accounts/login/"


@pytest.mark.django_db
def test_guest_user_required_with_authenticated(authenticated_client):
    """
    A registered user should not access sites only meant for guest users.

    """
    response = authenticated_client.get("/guest_user_required/")
    assert response.status_code == 302
    # authenticated users should be redirect to LOGIN_REDIRECT_URL
    assert response.url == "/accounts/profile/"


@pytest.mark.django_db
def test_guest_user_required_with_guest_user(client):
    # first request to become a guest user
    response = client.get("/allow_guest_user/")
    guest = response.context["user"]
    assert is_guest_user(guest)

    response = client.get("/guest_user_required/")

    assert response.status_code == 200
    # still the same guest user
    assert response.context["user"].id == guest.id


@pytest.mark.django_db
def test_regular_user_required_with_anonymous(client):
    response = client.get("/regular_user_required/")
    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/regular_user_required/"


@pytest.mark.django_db
def test_regular_user_required_with_guest(client):
    response = client.get("/allow_guest_user/")
    guest = response.context["user"]
    assert is_guest_user(guest)

    response = client.get("/regular_user_required/")
    assert response.status_code == 302
    # guest users should be redirect to the convert view instead
    assert response.url == "/convert/?next=/regular_user_required/"


@pytest.mark.django_db
def test_regular_user_required_with_authenticated(authenticated_client):
    response = authenticated_client.get("/regular_user_required/")
    assert response.status_code == 200
    response_user = response.context["user"]
    assert not response_user.is_anonymous
    assert response_user.username == "registered_user"
    assert not is_guest_user(response_user)
