from datetime import timedelta

import pytest
from django.utils.timezone import now
from guest_user.forms import UserCreationForm
from guest_user.functions import get_guest_model, is_guest_user
from guest_user.signals import converted


@pytest.mark.django_db
def test_manager_filter_expired():
    GuestModel = get_guest_model()

    for _i in range(3):
        GuestModel.objects.create_guest_user()

    old_user = GuestModel.objects.create_guest_user()
    # Force update the created_at timestamp
    GuestModel.objects.filter(user=old_user).update(
        created_at=now() - timedelta(days=25)
    )
    old_user.refresh_from_db()
    assert old_user.guest.is_expired(), old_user.guest.created_at

    assert GuestModel.objects.count() == 4
    assert GuestModel.objects.filter_expired().count() == 1


@pytest.mark.django_db
def test_manager_delete_expired():
    GuestModel = get_guest_model()

    for _i in range(3):
        GuestModel.objects.create_guest_user()

    GuestModel.objects.update(created_at=now() - timedelta(days=18))

    for _i in range(2):
        GuestModel.objects.create_guest_user()

    assert GuestModel.objects.count() == 5
    GuestModel.objects.delete_expired()
    assert GuestModel.objects.count() == 2


@pytest.mark.django_db
def test_convert_sends_signal():
    GuestModel = get_guest_model()
    guest_user = GuestModel.objects.create_guest_user()
    assert is_guest_user(guest_user)

    form = UserCreationForm(
        instance=guest_user,
        data={
            "username": "friendlyBaron45",
            "password1": "7mashedPotatoes",
            "password2": "7mashedPotatoes",
        },
    )
    assert form.is_valid(), form.errors

    signal_called = False

    def _handler(sender, user, **kwargs):
        nonlocal signal_called
        signal_called = True
        assert user == guest_user

    converted.connect(_handler)

    converted_user = GuestModel.objects.convert(form)

    assert signal_called

    assert not is_guest_user(converted_user)
    assert guest_user.id == converted_user.id
