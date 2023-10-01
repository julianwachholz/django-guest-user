from django.apps import AppConfig


class GuestUserConfig(AppConfig):
    name = "guest_user"
    verbose_name = "Guest User"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from . import checks  # noqa
