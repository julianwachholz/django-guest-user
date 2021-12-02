import re
from typing import List


class AppSettings:
    """
    This class holds guest user settings.

    Each property corresponds to a setting in the Django project
    prefixed with ``GUEST_USER_``.

    """

    def __init__(self, prefix):
        self.prefix = prefix

    def get(self, name, default):
        from django.conf import settings

        return getattr(settings, self.prefix + name, default)

    @property
    def NAME_GENERATOR(self) -> str:
        """
        Name generator function to use for temporary guest users.

        Included with the package are three generators:

        - ``guest_user.functions.generate_uuid_username`` (default)

            Generates a UUID4 as a username. Not intended to be shown to the visitor.
            This is the option with the smallest chance for collisions.

        - ``guest_user.functions.generate_numbered_username``

            Will create a random four digit number prefixed by ``GUEST_USER_NAME_PREFIX``.

        - ``guest_user.functions.generate_friendly_username``

            Creates a friendly and easy to remember username by combining an adjective, noun and number.
            Requires the `random_username <https://pypi.org/project/random-username/>`_ package.

        """
        return self.get("NAME_GENERATOR", "guest_user.functions.generate_uuid_username")

    @property
    def NAME_PREFIX(self) -> str:
        """
        Random username prefix used with ``generate_numbered_username``.

        :default: ``"Guest"``

        """
        return self.get("NAME_PREFIX", "Guest")

    @property
    def MAX_AGE(self) -> int:
        """
        Maximum age in seconds for guest sessions to stay valid.

        After this time the session may get deleted by background tasks.

        :default: ``SESSION_COOKIE_AGE``

        """
        max_age = self.get("MAX_AGE", None)
        if max_age is None:
            from django.conf import settings as django_settings

            max_age = django_settings.SESSION_COOKIE_AGE
        return max_age

    @property
    def CONVERT_FORM(self) -> str:
        """
        Import path for the form used to convert a guest to a real user.

        The form must have a method ``get_credentials`` to authenticate the user
        after registering.

        :default: ``"guest_user.forms.UserCreationForm"``

        """
        return self.get("CONVERT_FORM", "guest_user.forms.UserCreationForm")

    @property
    def CONVERT_PREFILL_USERNAME(self) -> bool:
        """
        Prefill the generated username in the conversion form.

        :default: ``False``

        """
        return self.get("CONVERT_PREFILL_USERNAME", False)

    @property
    def CONVERT_URL(self) -> str:
        """
        URL name for the convert view.

        :default: ``"guest_user_convert"``

        """
        return self.get("CONVERT_URL", "guest_user_convert")

    @property
    def CONVERT_REDIRECT_URL(self) -> str:
        """
        URL to redirect to after a successful conversion.

        This setting has no effect if a user starts the conversion process from
        a page where they were redirected from with a ``?next=/url/`` query string.

        :default: ``"guest_user_convert_success"``

        """
        return self.get("CONVERT_REDIRECT_URL", "guest_user_convert_success")

    @property
    def REQUIRED_ANON_URL(self) -> str:
        """
        Default redirect target when an anonymous visitor tries to access a view
        where a guest user is required.

        :default: ``LOGIN_URL``

        """
        url = self.get("REQUIRED_ANON_REDIRECT", None)
        if url is None:
            from django.conf import settings as django_settings

            url = django_settings.LOGIN_URL
        return url

    @property
    def REQUIRED_USER_URL(self) -> str:
        """
        Default redirect target when a registered user tries to access a view
        where a guest user is required.

        :default: ``LOGIN_REDIRECT_URL``

        """
        url = self.get("REQUIRED_USER_REDIRECT", None)
        if url is None:
            from django.conf import settings as django_settings

            url = django_settings.LOGIN_REDIRECT_URL
        return url

    # return type is the type for the setting, not return type of this property
    @property
    def BLOCKED_USER_AGENTS(self) -> List[str]:
        """
        A list of ignored user agents that will not create guest users.

        Items will be compiled together as a regular expression so you may use regex syntax.

        :default: Googlebot, Mediapartners-Google, Bingbot, Slurp, DuckDuckBot,
                  Baiduspider, Yandex(Mobile)?Bot, Sogou, Exabot, facebot, facebookexternalhit, ia_archiver

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
                "Yandex(Mobile)?Bot",
                "Sogou",
                "Exabot",
                "facebot",
                "facebookexternalhit",
                "ia_archiver",
            ],
        )

        expression = f"({ ')|('.join(blocked_uas) })"
        return re.compile(expression, re.IGNORECASE)

    @property
    def ENABLED(self) -> bool:
        """
        Disable guest users with this setting.

        :default: ``True``

        .. warning::

           The ``@allow_guest_user`` decorator will **not** enforce
           users to be authenticated if this setting is `False`.

        """
        return self.get("ENABLED", True)

    @property
    def MODEL(self) -> str:
        """
        Specify a different model to use for temporary guest users.

        :default: ``"guest_user.Guest"``

        """
        return self.get("MODEL", "guest_user.Guest")
