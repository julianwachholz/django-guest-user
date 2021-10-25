import re


class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def get(self, name, default):
        from django.conf import settings

        return getattr(settings, self.prefix + name, default)

    @property
    def ENABLED(self):
        """
        Disable guest users with this setting.

        The `@allow_guest_user` decorator will **not** enforce
        users to be authenticated if this setting is `False`.

        """
        return self.get("_ENABLED", True)

    @property
    def MODEL(self):
        """Specify a different model to use for temporary guest users."""
        return self.get("MODEL", "guest_user.Guest")

    @property
    def NAME_GENERATOR(self):
        """Name generator function to use for temporary guest users."""
        return self.get("NAME_GENERATOR", "guest_user.functions.generate_uuid_username")

    @property
    def NAME_PREFIX(self):
        """Random username prefix used with `generate_numbered_username`."""
        return self.get("NAME_PREFIX", "Guest")

    @property
    def MAX_AGE(self):
        """
        Maximum age in seconds for guest sessions to stay valid.

        After this time the session may get deleted by background tasks.

        """
        max_age = self.get("MAX_AGE", None)
        if max_age is None:
            from django.conf import settings as django_settings

            max_age = django_settings.SESSION_COOKIE_AGE
        return max_age

    @property
    def CONVERT_FORM(self):
        """
        Import path for the form used to convert a guest to a real user.

        The form must have a method `get_credentials` to authenticate the user
        after registering.

        """
        return self.get("CONVERT_FORM", "guest_user.forms.UserCreationForm")

    @property
    def CONVERT_PREFILL_USERNAME(self):
        """Prefill the generated username in the conversion form."""
        return self.get("CONVERT_PREFILL_USERNAME", False)

    @property
    def CONVERT_URL(self):
        """URL name for the convert view."""
        return self.get("CONVERT_URL", "guest_user_convert")

    @property
    def CONVERT_REDIRECT_URL(self):
        """
        URL to redirect to after a successful conversion.

        """
        return self.get("CONVERT_REDIRECT_URL", "guest_user_convert_success")

    @property
    def BLOCKED_USER_AGENTS(self):
        """
        A list of ignored user agents that will not create guest users.

        Items will be compiled together as a regular expression.

        """
        blocked_uas = self.get(
            "BLOCKED_USER_AGENTS",
            [
                "Googlebot",
                "Mediapartners-Google",
                "Bingbot",
                "Slurp",
                "DuckDuckBot",
                "Baiduspider",
                "YandexBot",
                "Sogou",
                "Exabot",
                "facebot",
                "facebookexternalhit",
                "ia_archiver",
            ],
        )

        expression = f"({ ')|('.join(blocked_uas) })"
        return re.compile(expression, re.IGNORECASE)


import sys  # noqa

app_settings = AppSettings("GUEST_USER_")
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
