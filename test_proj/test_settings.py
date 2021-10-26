import pytest
from guest_user.models import GuestManager


@pytest.mark.django_db
def test_setting_enabled(settings, client):
    settings.GUEST_USER_ENABLED = False

    response = client.get("/allow_guest_user/")
    assert response.status_code == 200
    assert response.context["user"].is_anonymous


def my_name_generator():
    return "custom_name"


def test_setting_name_generator(settings):
    settings.GUEST_USER_NAME_GENERATOR = "test_proj.test_settings.my_name_generator"
    assert GuestManager().generate_username() == "custom_name"
