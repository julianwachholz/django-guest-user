import re

import pytest
from django.contrib.auth import get_user_model
from guest_user.functions import get_guest_model, is_guest_user


@pytest.fixture
@pytest.mark.django_db
def authenticated_client(client):
    UserModel = get_user_model()
    user = UserModel.objects.create_user(username="registered_user")
    client.force_login(user)
    return client


@pytest.fixture
@pytest.mark.django_db
def guest_client(client):
    UserModel = get_user_model()
    GuestModel = get_guest_model()

    user = UserModel.objects.create_user(username="guest_user")
    GuestModel.objects.create(user=user)
    assert is_guest_user(user)

    client.force_login(user)
    client.user = user
    return client


class re_match:
    """Match a regular expression and show readable output."""

    def __init__(self, pattern: str, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return self._regex.match(actual) is not None

    def __repr__(self):
        return self._regex.pattern
