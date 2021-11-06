import pytest
from guest_user.functions import is_guest_user
from guest_user.signals import guest_created

# see views.py for view functions used in these tests
# this file, despite its name, also tests the class based mixins
# as they are all based on the functions in the `helper` module


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["/allow_guest_user/", "/mixin/allow_guest_user/"])
def test_allow_guest_user_with_anonymous(client, url):
    """
    Unauthenticated visitors get automatically logged in as a guest user.
    """
    response = client.get(url)

    assert response.status_code == 200
    user = response.context["user"]
    assert not user.is_anonymous
    assert len(user.username) == 32  # uuid4 length
    assert is_guest_user(user)


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["/allow_guest_user/", "/mixin/allow_guest_user/"])
def test_allow_guest_user_sends_signal(client, url):
    """
    Check that the guest_created signal is sent with the current request.

    """

    def post_guest_created(sender, user, request, **kwargs):
        """Add some data after a guest was created."""

        useragent = request.META.get("HTTP_USER_AGENT", "")
        user.first_name = f"A {useragent} user"
        user.save()

    guest_created.connect(post_guest_created)

    response = client.get(url, **{"HTTP_USER_AGENT": "Firefox"})
    assert response.status_code == 200
    user = response.context["user"]
    assert user.first_name == "A Firefox user"


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["/allow_guest_user/", "/mixin/allow_guest_user/"])
def test_allow_guest_user_ignores_robots(client, url):
    """
    No guest user is created for web crawlers etc. on the block list.

    """
    response = client.get(
        url,
        **{
            "HTTP_USER_AGENT": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        },
    )

    assert response.status_code == 200
    user = response.context["user"]
    assert user.is_anonymous
    assert not is_guest_user(user)


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["/allow_guest_user/", "/mixin/allow_guest_user/"])
def test_allow_guest_user_with_authenticated(authenticated_client, url):
    """
    Authenticated visitors should stay logged in.
    """
    response = authenticated_client.get(url)
    assert response.status_code == 200
    response_user = response.context["user"]
    assert not response_user.is_anonymous
    assert response_user.username == "registered_user"
    assert not is_guest_user(response_user)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url", ["/guest_user_required/", "/mixin/guest_user_required/"]
)
def test_guest_user_required_with_anonymous(client, url):
    """
    If a visitor isn't a guest user yet, they should
    be redirected to the login page.

    """
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == "/accounts/login/"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url", ["/guest_user_required/", "/mixin/guest_user_required/"]
)
def test_guest_user_required_with_authenticated(authenticated_client, url):
    """
    A registered user should not access sites only meant for guest users.

    """
    response = authenticated_client.get(url)
    assert response.status_code == 302
    # authenticated users should be redirect to LOGIN_REDIRECT_URL
    assert response.url == "/accounts/profile/"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url", ["/guest_user_required/", "/mixin/guest_user_required/"]
)
def test_guest_user_required_with_guest_user(guest_client, url):
    response = guest_client.get(url)

    assert response.status_code == 200
    # still the same guest user
    assert response.context["user"].id == guest_client.user.id


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url", ["/regular_user_required/", "/mixin/regular_user_required/"]
)
def test_regular_user_required_with_anonymous(client, url):
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == f"/accounts/login/?next={url}"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url", ["/regular_user_required/", "/mixin/regular_user_required/"]
)
def test_regular_user_required_with_guest(guest_client, url):
    response = guest_client.get(url)
    assert response.status_code == 302
    # guest users should be redirect to the convert view instead
    assert response.url == f"/convert/?next={url}"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "url", ["/regular_user_required/", "/mixin/regular_user_required/"]
)
def test_regular_user_required_with_authenticated(authenticated_client, url):
    response = authenticated_client.get(url)
    assert response.status_code == 200
    response_user = response.context["user"]
    assert not response_user.is_anonymous
    assert response_user.username == "registered_user"
    assert not is_guest_user(response_user)
