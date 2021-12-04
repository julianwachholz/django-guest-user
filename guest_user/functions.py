import random
import uuid
from urllib.parse import urlparse

from django.apps import apps as django_apps
from django.contrib.auth import authenticate, get_user_model, login
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import resolve_url

from . import settings


def maybe_create_guest_user(request):
    """
    Create a guest user and log them in.

    This function will create and authenticate a new guest user should the visitor
    not be authenticated already and their user agent isn't on the block list.

    """
    assert hasattr(
        request, "session"
    ), "Please add 'django.contrib.sessions' to INSTALLED_APPS."

    if settings.ENABLED and request.user.is_anonymous:
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        if not settings.BLOCKED_USER_AGENTS.search(user_agent):
            Guest = get_guest_model()
            user = Guest.objects.create_guest_user(request)
            user = authenticate(request=request, username=user.username)
            assert user, (
                "Guest authentication failed. Do you have "
                "'guest_user.backends.GuestBackend' in AUTHENTICATION_BACKENDS?"
            )
            login(request, user)


def get_guest_model():
    """
    Return the configured Guest model.
    """
    try:
        return django_apps.get_model(settings.MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "GUEST_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "GUEST_USER_MODEL refers to model '%s' that has not been installed"
            % settings.MODEL
        )


def is_guest_user(user) -> bool:
    """
    Check if the given user instance is a temporary guest.

    """

    if user.is_anonymous:
        return False

    if getattr(user, "backend", None) == "guest_user.backends.GuestBackend":
        return True

    GuestModel = get_guest_model()
    return GuestModel.objects.filter(user=user).exists()


def generate_uuid_username() -> str:
    """Generate a random username based on UUID."""
    UserModel = get_user_model()
    max_length = UserModel._meta.get_field(UserModel.USERNAME_FIELD).max_length
    return uuid.uuid4().hex[:max_length]


def generate_numbered_username() -> str:
    """Generate a random username based on a prefix and a random number."""
    prefix = settings.NAME_PREFIX
    digits = settings.NAME_SUFFIX_DIGITS
    number = random.randint(1, (10 ** digits) - 1)
    return f"{prefix}{number:{f'0{digits}'}}"


def generate_friendly_username() -> str:
    """
    Generate a random username with adjective and nouns put together.

    Requires `random-username` to be installed.
    """
    from random_username.generate import generate_username

    return generate_username()[0]


def redirect_with_next(request, redirect_url, redirect_field_name):
    """
    Redirect the user to a login page with a "next" parameter.

    :meta private:

    """
    # https://github.com/django/django/blob/ba9ced3e9a643a05bc521f0a2e6d02e3569de374/django/contrib/auth/decorators.py#L22-L33  # noqa

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
