from functools import wraps
from urllib.parse import urlparse

from django.conf import settings as django_settings
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login
from django.shortcuts import redirect, resolve_url

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
            if not settings.BLOCKED_USER_AGENTS.search(user_agent):
                Guest = get_guest_model()
                user = Guest.objects.create_guest_user(request)
                user = authenticate(username=user.username)
                assert user, (
                    "Guest authentication failed. Do you have "
                    "'guest_user.backends.GuestBackend' in AUTHENTICATION_BACKENDS?"
                )
                login(request, user)

        return function(request, *args, **kwargs)

    return wraps(function)(wrapped)


def guest_user_required(
    function=None,
    anonymous_url=None,
    registered_url=None,
):
    """
    Current user must be a temporary guest.

    Anonymous users will be redirected to `anonymous_url`.
    Registered users will be redirected to `registered_url`.

    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if is_guest_user(request.user):
                return view_func(request, *args, **kwargs)
            if request.user.is_anonymous:
                redirect_url = anonymous_url or settings.REQUIRED_ANON_URL
            else:
                redirect_url = registered_url or settings.REQUIRED_USER_URL
            return redirect(redirect_url)

        return wrapper

    if function:
        return decorator(function)
    return decorator


def regular_user_required(
    function=None,
    login_url=None,
    convert_url=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
):
    """
    Current user must not be a temporary guest.

    Guest users will be redirected to the `convert_url`.
    Anonymous users will be redirected to `login_url`.

    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and not is_guest_user(user):
                return view_func(request, *args, **kwargs)

            if user.is_anonymous:
                redirect_url = login_url or django_settings.LOGIN_URL
            else:
                redirect_url = convert_url or settings.CONVERT_URL
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(redirect_url)

            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if (not login_scheme or login_scheme == current_scheme) and (
                not login_netloc or login_netloc == current_netloc
            ):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(path, resolved_login_url, redirect_field_name)

        return wrapper

    if function:
        return decorator(function)
    return decorator
