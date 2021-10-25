import pytest
from django.contrib.auth import get_user_model
from guest_user.functions import get_guest_model, is_guest_user


@pytest.mark.django_db
def test_is_guest_user():
    UserModel = get_user_model()
    user = UserModel.objects.create_user("dummy")

    assert is_guest_user(user) is False

    GuestModel = get_guest_model()
    GuestModel.objects.create(user=user)
    assert is_guest_user(user) is True
