import pytest
from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth import get_user_model
from guest_user.contrib.allauth.signals import converted_social_account
from guest_user.functions import is_guest_user

from .conftest import re_match


@pytest.mark.django_db
def test_allauth_connect(rf, guest_client):
    """
    Send a `social_account_added` signal for a guest user.

    Expect a signal receiver to convert the guest user using
    the newly connected social account from allauth.

    """
    # let's convert this guest user
    user = guest_client.user

    # Use the RequestFactory to mock a request to the callback of a OAuth2 callback endpoint
    request = rf.get("/accounts/twitter/login/callback/")
    request.user = user

    social_username = "converting_user"

    signal_called = False

    def _handler(sender, user, sociallogin, **kwargs):
        nonlocal signal_called
        signal_called = True
        assert str(sociallogin.account) == social_username

    converted_social_account.connect(_handler)

    # By signing in to their fake twitter account...
    # The Twitter provider for example will first try to use the "screen_name" attribute
    socialaccount = SocialAccount(
        user=user,
        provider="twitter",
        uid="1234567",
        extra_data={
            "screen_name": social_username,
        },
    )
    sociallogin = SocialLogin(user=user, account=socialaccount)
    # https://github.com/pennersr/django-allauth/blob/353386216b79f16709e97bb487c0bbbba2bc0c71/allauth/socialaccount/helpers.py#L121
    social_account_added.send(
        sender=SocialLogin, request=request, sociallogin=sociallogin
    )

    assert signal_called
    assert not is_guest_user(user)
    assert user.username == social_username


@pytest.mark.django_db
def test_allauth_connect_username_taken(rf, guest_client):
    """
    A user tries to convert using a social account but
    their connected account's username is already taken.

    """
    # register a user that has the same username as the guest's twitter account
    taken_username = "taken_username"
    UserModel = get_user_model()
    UserModel.objects.create(username=taken_username)

    user = guest_client.user
    request = rf.get("/accounts/twitter/login/callback/")
    request.user = user

    socialaccount = SocialAccount(
        user=user,
        provider="twitter",
        uid="567890",
        extra_data={
            # We set both the screen_name and name attribute to the desired username,
            # because allauth falls back to it if the screen name isn't available.
            "name": taken_username,
            "screen_name": taken_username,
        },
    )
    sociallogin = SocialLogin(user=user, account=socialaccount)
    social_account_added.send(
        sender=SocialLogin, request=request, sociallogin=sociallogin
    )

    assert not is_guest_user(user)

    # Allauth will by default append a single numeral to an already taken username
    assert user.username == re_match(r"^%s\d+$" % taken_username)
