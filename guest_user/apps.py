from django.apps import AppConfig


class GuestUserConfig(AppConfig):
    name = "guest_user"
    verbose_name = "Guest User"

    def ready(self):
        from . import checks  # noqa
