from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .functions import is_guest_user


class GuestBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate with username only."""
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
            # user.backend = "guest_user.backends.GuestBackend"
        except UserModel.DoesNotExist:
            return None
        return user
