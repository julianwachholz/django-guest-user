import sys  # noqa

from .app_settings import AppSettings

app_settings = AppSettings("GUEST_USER_")
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
