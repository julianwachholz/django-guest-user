# django-guest-user

A Django app that allows visitors to interact with your site as a guest user
without requiring registration.

Largely inspired by [django-lazysignup](https://github.com/danfairs/django-lazysignup) and rewritten for Django 3 and Python 3.6 and up.

## Installation

Install the package with your favorite package manager from PyPI:

```
pip install django-guest-user
```

Add the app to your `INSTALLED_APPS` and `AUTHENTICATION_BACKENDS`:

```python
INSTALLED_APPS = [
    ...
    "guest_user",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guest_user.backends.GuestBackend",
]
```

Add the patterns to your URL config:

```python
urlpatterns = [
    ...
    path("convert/", include("guest_user.urls")),
]
```

Don't forget to run migrations:

```
python manage.py migrate
```

## How to use

Guest users are not created for every unauthenticated request.
Instead, use the `@allow_guest_user` decorator on a view to enable
that view to be accessed by a temporary guest user.

```python
from guest_user.decorators import allow_guest_user

@allow_guest_user
def my_view(request):
    # Will always be either a registered a guest user.
    username = request.user.username
    return HttpResponse(f"Hello, {username}!")
```

## API

### `@guest_user.decorators.allow_guest_user`

View decorator that will create a temporary guest user in the event
that the decorated view is accessed by an unauthenticated visitor.

Takes no arguments.

### `@guest_user.decorators.guest_user_required(redirect_field_name="next", login_url=None)`

View decorator that redirects to a given URL if the accessing user is
anonymous or already authenticated.

Arguments:

- `redirect_field_name`: URL query parameter to use to link back in the case of a redirect to the login url. Defaults to `django.contrib.auth.REDIRECT_FIELD_NAME` ("next").
- `login_url`: URL to redirect to if the user is not authenticated. Defaults to the `LOGIN_URL` setting.

### `@guest_user.decorators.regular_user_required(redirect_field_name="next", login_url=None)`

Decorator that will not allow guest users to access the view.
Will redirect to the conversion page to allow a guest user to fully register.

Arguments:

- `redirect_field_name`: URL query parameter to use to link back in the case of a redirect to the login url. Defaults to `django.contrib.auth.REDIRECT_FIELD_NAME` ("next").
- `login_url`: URL to redirect to if the user is a guest. Defaults to `"guest_user_convert"`.

### `guest_user.functions.get_guest_model()`

The guest user model is swappable. This function will return the currently configured model class.

### `guest_user.functions.is_guest_user(user)`

Check wether the given user instance is a temporary guest.

### `guest_user.signals.converted`

Signal that is dispatched when a guest user is converted to a regular user.

### Template tag `is_guest_user`

A filter to use in templates to check if the user object is a guest.

```
{% load guest_user %}

{% if user|is_guest_user %}
  Hello guest.
{% endif %}
```

## Settings

Various settings are provided to allow customization of the guest user behavior.

### `GUEST_USER_ENABLED`

`bool`. If `False`, the `@allow_guest_user` decorator will not create guest users.
Defaults to `True`.

### `GUEST_USER_MODEL`

`str`. The swappable model identifier to use as the guest model.
Defaults to `"guest_user.Guest"`.

### `GUEST_USER_NAME_GENERATOR`

`str`. Import path to a function that will generate a username for a guest user.
Defaults to `"guest_user.functions.generate_uuid_username"`.

Included with the package are two alternatives:

`"guest_user.functions.generate_numbered_username"`: Will create a random four digit
number prefixed by `GUEST_USER_NAME_PREFIX`.

`"guest_user.functions.generate_friendly_username"`: Creates a friendly and easy to remember username by combining an adjective, noun and number. Requires `random_username` to be installed.

### `GUEST_USER_NAME_PREFIX`

`str`. A prefix to use with the `generate_numbered_username` generator.
Defaults to `"Guest"`.

### `GUEST_USER_MAX_AGE`

`int`. Seconds to keep a guest user before expiring.
Defaults to `settings.SESSION_COOKIE_AGE`.

### `GUEST_USER_CONVERT_FORM`

`str`. Import path for the guest conversion form.
Must implement `get_credentials` to be passed to Django's `authenticate` function.
Defaults to `"guest_user.forms.UserCreationForm"`.

### `GUEST_USER_CONVERT_PREFILL_USERNAME`

`bool`. Set the generated username as initial value on the conversion form.
Defaults to `False`.

### `GUEST_USER_CONVERT_URL`

`str`. URL name for the convert view.
Defaults to `"guest_user_convert"`.

### `GUEST_USER_CONVERT_REDIRECT_URL`

`str`. URL name to redirect to after conversion, unless a redirect parameter was provided.
Defaults to `"guest_user_convert_success"`.

### `GUEST_USER_BLOCKED_USER_AGENTS`

`list[str]`. Web crawlers and other user agents to block from becoming guest users.
The list will be combined into a regular expression.
Default includes a number of well known bots and spiders.

## Status

This project is currently untested. But thanks to [previous work](https://github.com/danfairs/django-lazysignup) it is largely functional.

I decided to rewrite the project since the original project hasn't seen any
larger updates for a few years now and the code base was written a long time ago.
