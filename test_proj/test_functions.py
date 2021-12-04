import pytest
from django.contrib.auth import get_user_model
from guest_user.functions import (
    generate_numbered_username,
    generate_uuid_username,
    get_guest_model,
    is_guest_user,
)


@pytest.mark.django_db
def test_is_guest_user():
    UserModel = get_user_model()
    user = UserModel.objects.create_user("dummy")

    assert is_guest_user(user) is False

    GuestModel = get_guest_model()
    GuestModel.objects.create(user=user)
    assert is_guest_user(user) is True


def test_generate_uuid_username():
    uuid_username = generate_uuid_username()
    assert len(uuid_username) == 32
    assert uuid_username.isalnum()


def test_generate_uuid_username_unique():
    """Ensure no duplicates for a lot of usernames."""
    count = 10000
    names = {generate_uuid_username() for _ in range(count)}
    assert len(names) == count


def test_generate_numbered_username():
    numbered_username = generate_numbered_username()
    assert len(numbered_username) == 9
    assert numbered_username.startswith("Guest")
    assert numbered_username[-4:].isdigit()


def test_generate_numbered_username_custom(settings):
    """Customize the numbered username generator with settings."""
    settings.GUEST_USER_NAME_PREFIX = "Gast"
    numbered_username = generate_numbered_username()
    assert len(numbered_username) == 8
    assert numbered_username.startswith("Gast")
    assert numbered_username[-4:].isdigit()

    settings.GUEST_USER_NAME_PREFIX = "anonymous#"
    settings.GUEST_USER_NAME_SUFFIX_DIGITS = 5
    anon_username = generate_numbered_username()
    assert len(anon_username) == 15
    assert anon_username.startswith("anonymous#")
    assert anon_username[-5:].isdigit()


def test_generate_numbered_username_unique():
    """A four digit number can only have so many unique random numbers."""
    count = 1000  # 10% of a 4 digit number space
    names = {generate_numbered_username() for _ in range(count)}
    assert len(names) > 900  # still enough?
