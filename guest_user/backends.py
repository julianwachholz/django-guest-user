from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured

from .functions import is_guest_user


class GuestBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate with username only."""
        if password is not None:
            raise ImproperlyConfigured(
                "The GuestBackend received a password argument. This is likely a configuration error. "
                "Please ensure that Guestbackend is the last entry in AUTHENTICATION_BACKENDS."
            )
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(**{UserModel.USERNAME_FIELD: username})
        except UserModel.DoesNotExist:
            return None
        if is_guest_user(user):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user
