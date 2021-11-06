from django.conf import settings as django_settings
from django.core.checks import Error, Warning, register

from . import settings


@register()
def check_settings(app_configs, **kwargs):
    checks = []

    guest_backend = "guest_user.backends.GuestBackend"

    if (
        settings.ENABLED
        and guest_backend not in django_settings.AUTHENTICATION_BACKENDS
    ):
        checks.append(
            Error(
                "The GuestBackend is not in your AUTHENTICATION_BACKENDS. Authenticating guest users will not work.",
                hint='Add "guest_user.backends.GuestBackend" to the AUTHENTICATION_BACKENDS setting.',
                obj="settings",
                id="guest_user.W001",
            )
        )
    elif (
        settings.ENABLED
        and django_settings.AUTHENTICATION_BACKENDS[-1] != guest_backend
    ):
        checks.append(
            Warning(
                "The GuestBackend is not the last item in AUTHENTICATION_BACKENDS. This may have unintended effects.",
                hint='Move the "guest_user.backends.GuestBackend" to the last item in the list.',
                obj="settings",
                id="guest_user.W001",
            )
        )

    return checks
