import pytest
from django.contrib.auth import get_user_model
from guest_user.backends import GuestBackend
from guest_user.functions import get_guest_model


@pytest.fixture
def backend():
    return GuestBackend()


@pytest.mark.django_db
def test_backend_without_user(backend):
    assert backend.authenticate(request=None, username="doesnotexist") is None


@pytest.mark.django_db
def test_backend_does_not_authenticate_normal_user(backend):
    UserModel = get_user_model()
    user = UserModel.objects.create_user(username="demo", password="hunter2")
    assert backend.authenticate(request=None, username=user.username) is None


@pytest.mark.django_db
def test_backend_authenticates_guest_user(backend):
    GuestModel = get_guest_model()
    guest = GuestModel.objects.create_guest_user()

    backend_guest = backend.authenticate(request=None, username=guest.username)
    assert backend_guest.username == guest.username
