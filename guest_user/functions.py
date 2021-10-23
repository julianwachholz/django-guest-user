import random
import uuid

from django.apps import apps as django_apps
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured

from . import settings


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
    """Check if the given user instance is a temporary guest."""

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
    number = random.randint(1, 9999)
    return f"{prefix}{number:04}"


def generate_friendly_username() -> str:
    """
    Generate a random username with adjective and nouns put together.

    Requires `random-username` to be installed.
    """
    from random_username.generate import generate_username

    return generate_username()[0]
