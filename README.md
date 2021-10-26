[![Code Lint](https://github.com/julianwachholz/django-guest-user/actions/workflows/lint.yml/badge.svg)](https://github.com/julianwachholz/django-guest-user/actions/workflows/lint.yml)
[![Python Tests](https://github.com/julianwachholz/django-guest-user/actions/workflows/test.yml/badge.svg)](https://github.com/julianwachholz/django-guest-user/actions/workflows/test.yml)

# django-guest-user

A Django app that allows visitors to interact with your site as a guest user
without requiring registration.

Largely inspired by [django-lazysignup](https://github.com/danfairs/django-lazysignup) and rewritten for Django 3.1+ and Python 3.7+.

## Requirements

The tests cover the following versions:

- Python 3.7, 3.8, 3.9
- Django 3.1, 3.2 and `main`

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

Guest users are not created for every unauthenticated request. Instead, use the
`@allow_guest_user` decorator on a view to enable that view to be accessed by
a temporary guest user.

```python
from guest_user.decorators import allow_guest_user

@allow_guest_user
def my_view(request):
    # Will always be either a registered a guest user.
    username = request.user.username
    return HttpResponse(f"Hello, {username}!")
```

Each time an anonymous user requests this view, the decorator will create a new
temporary guest user and automatically create a session for them.

If some parts of the application should not be used by guests, you can use the
`@require_regular_user` decorator to disable guest access.

At any point in time, the guest user may choose to permanently register with
the website by using the conversion view.

## API

### Decorators

Module: `guest_user.decorators`

#### `@allow_guest_user`

View decorator that will create a temporary guest user in the event that the
decorated view is accessed by an unauthenticated visitor.

Takes no arguments.

#### `@guest_user_required`

View decorator that only allows guest users. Anonymous or registered users will
be redirected to their respective redirect targets.

```python
@guest_user_required(anonymous_url="/login/", registered_url="/dashboard/")
def only_for_guests(request):
    pass
```

Arguments:

- `anonymous_url`: Redirect target for anonymous users.
  Defaults to the `GUEST_USER_REQUIRED_ANON_URL` setting.
- `registered_url`: Redirect target for registered users.
  Defaults to the `GUEST_USER_REQUIRED_USER_URL` setting.

#### `@regular_user_required`

Decorator that will not allow guest users to access the view.
Will redirect to the conversion page to allow a guest user to fully register.

```python
@regular_user_required(login_url="/login/", convert_url="/convert/")
def only_for_real_users(request):
    pass
```

Arguments:

- `login_url`: Redirect target for anonymous users.
  Defaults to the `GUEST_USER_REQUIRED_ANON_URL` setting.
- `convert_url`: Redirect target for **guest** users.
  Defaults to the `GUEST_USER_REQUIRED_USER_URL` setting.
- `redirect_field_name`: URL parameter used to redirect to the origin page.
  Defaults to `django.contrib.auth.REDIRECT_FIELD_NAME` (`"next"`).

### Functions

Module: `guest_user.functions`

#### `is_guest_user(user)`

Check wether the given user instance is a temporary guest.

Returns `bool`.

### Signals

Module: `guest_user.signals`

#### `guest_created(user, request)`

Signal dispatched when a visitor accessed a view that created a guest user.

Provides `user` and `request` arguments.

#### `converted(user)`

Signal dispatched when a guest user is converted to a regular user.

Provides `user` and `request` arguments.

### Template Tags

### `is_guest_user`

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

### `GUEST_USER_REQUIRED_ANON_URL`

`str`. URL name to redirect to when an anonymous visitor tries to access a view
with the `@guest_user_required` decorator.
Defaults to `settings.LOGIN_URL`.

### `GUEST_USER_REQUIRED_USER_URL`

`str`. URL name to redirect to when a registered user tries to access a view
with the `@guest_user_required` decorator.
Defaults to `settings.LOGIN_REDIRECT_URL`.

### `GUEST_USER_BLOCKED_USER_AGENTS`

`list[str]`. Web crawlers and other user agents to block from becoming guest users.
The list will be combined into a regular expression.
Default includes a number of well known bots and spiders.

## Status

This project is still under development. But thanks to [previous work](https://github.com/danfairs/django-lazysignup) it is largely functional.

I decided to rewrite the project since the original project hasn't seen any
larger updates for a few years now. The initial code base was written a long
time ago as well.
