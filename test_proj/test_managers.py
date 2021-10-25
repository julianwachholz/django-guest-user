import pytest
from guest_user.forms import UserCreationForm
from guest_user.functions import get_guest_model, is_guest_user
from guest_user.signals import converted


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
