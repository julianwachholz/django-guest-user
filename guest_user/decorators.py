from functools import wraps

from django.conf import settings as django_settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect

from . import settings
from .functions import is_guest_user, maybe_create_guest_user, redirect_with_next


def allow_guest_user(function=None):
    """
    Allow anonymous users to access the view by creating a guest user.

    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            maybe_create_guest_user(request)
            return view_func(request, *args, **kwargs)

        return wrapper

    if function:
        return decorator(function)
    return decorator


def guest_user_required(
    function=None,
    anonymous_url=None,
    registered_url=None,
):
    """
    Current user must be a temporary guest.

    Anonymous users will be redirected to `anonymous_url`.
    Registered users will be redirected to `registered_url`.

    Since being a guest user is not a state that a registered
    user can ever revert back to, there is no "next" URL handling
    in this decorator.

    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if is_guest_user(request.user):
                return view_func(request, *args, **kwargs)
            if request.user.is_anonymous:
                redirect_url = anonymous_url or settings.REQUIRED_ANON_URL
            else:
                redirect_url = registered_url or settings.REQUIRED_USER_URL
            return redirect(redirect_url)

        return wrapper

    if function:
        return decorator(function)
    return decorator


def regular_user_required(
    function=None,
    login_url=None,
    convert_url=None,
    redirect_field_name=REDIRECT_FIELD_NAME,
):
    """
    Current user must not be a temporary guest.

    Anonymous users will be redirected to `login_url`.
    Guest users will be redirected to the `convert_url`.

    The redirected URL will get a "next" parameter added to the URL
    in order to redirect the user back to the page they were trying to access.

    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and not is_guest_user(user):
                return view_func(request, *args, **kwargs)
            if user.is_anonymous:
                redirect_url = login_url or django_settings.LOGIN_URL
            else:
                redirect_url = convert_url or settings.CONVERT_URL
            return redirect_with_next(request, redirect_url, redirect_field_name)

        return wrapper

    if function:
        return decorator(function)
    return decorator
