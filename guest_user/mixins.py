from django.conf import settings as django_settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect

from . import settings
from .functions import is_guest_user, maybe_create_guest_user, redirect_with_next


class AllowGuestUserMixin:
    """
    Allow anonymous users to access the view by creating a guest user.

    """

    def dispatch(self, request, *args, **kwargs):
        maybe_create_guest_user(request)
        return super().dispatch(request, *args, **kwargs)


class GuestUserRequiredMixin:
    """
    Current user must be a temporary guest.

    Anonymous users will be redirected to `anonymous_url`.
    Registered users will be redirected to `registered_url`.

    Since being a guest user is not a state that a registered
    user can ever revert back to, there is no "next" URL handling
    in this mixin.

    """

    anonymous_url = None
    registered_url = None

    def dispatch(self, request, *args, **kwargs):
        if is_guest_user(request.user):
            return super().dispatch(request, *args, **kwargs)
        if request.user.is_anonymous:
            redirect_url = self.anonymous_url or settings.REQUIRED_ANON_URL
        else:
            redirect_url = self.registered_url or settings.REQUIRED_USER_URL
        return redirect(redirect_url)


class RegularUserRequiredMixin:
    """
    Current user must not be a temporary guest.

    Anonymous users will be redirected to `login_url`.
    Guest users will be redirected to the `convert_url`.

    The redirected URL will get a "next" parameter added to the URL
    in order to redirect the user back to the page they were trying to access.

    """

    login_url = None
    convert_url = None
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_login_url(self):
        if not self.request.user.is_anonymous:
            return self.convert_url or settings.CONVERT_URL
        return super().get_login_url()

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and not is_guest_user(user):
            return super().dispatch(request, *args, **kwargs)
        if user.is_anonymous:
            redirect_url = self.login_url or django_settings.LOGIN_URL
        else:
            redirect_url = self.convert_url or settings.CONVERT_URL
        return redirect_with_next(request, redirect_url, self.redirect_field_name)
