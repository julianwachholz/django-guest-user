from django.apps import AppConfig


class GuestUserAllauthConfig(AppConfig):
    name = "guest_user.contrib.allauth"
    label = "guest_user_allauth"
    verbose_name = "Guest User Allauth Contrib"

    def ready(self):
        from . import signals  # noqa
