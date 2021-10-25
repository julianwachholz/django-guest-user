from guest_user.models import GuestManager


def my_name_generator():
    return "custom_name"


def test_setting_name_generator(settings):
    settings.GUEST_USER_NAME_GENERATOR = "test_proj.test_settings.my_name_generator"
    assert GuestManager().generate_username() == "custom_name"
