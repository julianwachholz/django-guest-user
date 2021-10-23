from functools import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login
from django.contrib.auth.decorators import user_passes_test

from . import settings
from .functions import get_guest_model, is_guest_user


def allow_guest_user(function=None):
    """
    Allow anonymous users to access the view by creating a guest user.

    """

    def wrapped(request, *args, **kwargs):
        assert hasattr(
            request, "session"
        ), "Please add 'django.contrib.sessions' to INSTALLED_APPS."

        if settings.ENABLED and request.user.is_anonymous:
            user_agent = request.META.get("HTTP_USER_AGENT", "")

            if not settings.BLOCKED_USER_AGENTS.match(user_agent):
                Guest = get_guest_model()
                user = Guest.objects.create_guest_user()
                # request.user = None
                user = authenticate(username=user.username)
                assert user, (
                    "Guest authentication failed. Do you have "
                    "'guest_user.backends.GuestBackend' in AUTHENTICATION_BACKENDS?"
                )
                login(request, user)

        return function(request, *args, **kwargs)

    return wraps(function)(wrapped)


def guest_user_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Current user must be a temporary guest.

    Other visitors will be redirected to `login_url` or a redirect parameter given in the URL.

    """
    actual_decorator = user_passes_test(
        is_guest_user,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def regular_user_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, convert_url=None
):
    """
    Current user must not be a temporary guest.

    Guest users will be redirected to the convert page.

    """
    if convert_url is None:
        convert_url = settings.CONVERT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and not is_guest_user(u),
        login_url=convert_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
