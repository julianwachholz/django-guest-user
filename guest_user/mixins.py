from django.conf import settings as django_settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect

from . import settings
from .functions import is_guest_user, maybe_create_guest_user, redirect_with_next


class AllowGuestUserMixin:
    """
    Allow anonymous users to access the view by creating a guest user.

    This mixin does not require overriding any attributes.

    Example usage:

    .. code:: python

        from guest_user.mixins import AllowGuestUserMixin

        class HelloWorldView(AllowGuestUserMixin, View):
            def get(self, request):
                return HttpResponse(f"Hello {request.user.username}!")

    """

    def dispatch(self, request, *args, **kwargs):
        maybe_create_guest_user(request)
        return super().dispatch(request, *args, **kwargs)


class GuestUserRequiredMixin:
    """
    Current user must be a temporary guest.

    Since being a guest user is not a state that a registered
    user can ever revert back to, there is no "next" URL handling
    in this mixin.

    Example usage:

    .. code:: python

        from guest_user.mixins import GuestUserRequiredMixin

        class OnlyGuestView(GuestUserRequiredMixin, View):
            anonymous_url = "/login/"
            registered_url = "/dashboard/"

    """

    anonymous_url: str = None
    """
    Redirect target for anonymous users.
    Defaults to :attr:`GUEST_USER_REQUIRED_ANON_URL<guest_user.app_settings.AppSettings.REQUIRED_ANON_URL>`.
    """

    registered_url: str = None
    """
    Redirect target for registered users.
    Defaults to :attr:`GUEST_USER_REQUIRED_USER_URL<guest_user.app_settings.AppSettings.REQUIRED_USER_URL>`.
    """

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

    Example usage:

    .. code:: python

        from guest_user.mixins import RegularUserRequiredMixin

        class RealUsersOnlyView(RegularUserRequiredMixin, View):
            login_url = "/login/"
            convert_url = "/convert/?from=RealUsersOnlyView"

    """

    login_url: str = None
    """
    Redirect target for anonymous users.
    Defaults to :ref:`django:ref/settings:``login_url```.
    """

    convert_url: str = None
    """
    Redirect target for guest users.
    Defaults to :attr:`GUEST_USER_CONVERT_URL<guest_user.app_settings.AppSettings.CONVERT_URL>`.
    """

    redirect_field_name: str = REDIRECT_FIELD_NAME
    """
    URL parameter used to redirect to the origin page. Defaults to
    :attr:`django.contrib.auth.REDIRECT_FIELD_NAME<django:django.contrib.auth.mixins.AccessMixin.redirect_field_name>`
    (= "next").
    """

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
