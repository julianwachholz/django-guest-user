import pytest
from guest_user.functions import is_guest_user
from guest_user.models import Guest


@pytest.mark.django_db
def test_unique_usernames():
    """The manager avoids duplicate guest usernames."""
    guest1 = Guest.objects.create_guest_user(username="username_conflict")
    guest2 = Guest.objects.create_guest_user(username="username_conflict")
    assert guest1.username != guest2.username


@pytest.mark.django_db
def test_create_guest_user():
    guest = Guest.objects.create_guest_user()
    assert is_guest_user(guest)
