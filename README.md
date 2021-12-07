[![Code Lint](https://github.com/julianwachholz/django-guest-user/actions/workflows/lint.yml/badge.svg)](https://github.com/julianwachholz/django-guest-user/actions/workflows/lint.yml)
[![Python Tests](https://github.com/julianwachholz/django-guest-user/actions/workflows/test.yml/badge.svg)](https://github.com/julianwachholz/django-guest-user/actions/workflows/test.yml)
[![Documentation](https://readthedocs.org/projects/django-guest-user/badge/?style=flat)](https://django-guest-user.readthedocs.io)

# django-guest-user

Allow visitors to interact with your site like a temporary user ("guest")
without requiring registration.

Anonymous visitors who request a decorated page get a real temporary user object
assigned and are logged in automatically. They can use the site like a normal
user until they decide to convert to a real user account to save their data.

Inspired by and as an alternative for [django-lazysignup](https://github.com/danfairs/django-lazysignup)
and rewritten for Django 3.1+ and Python 3.7+.

## Documentation

Find the [**complete documentation**](https://django-guest-user.readthedocs.io/)
on Read the Docs.

## Quickstart

1. Install the `django-guest-user` package from PyPI
2. Add `guest_user` to your `INSTALLED_APPS` and migrate your database
3. Add `guest_user.backends.GuestBackend` to your `AUTHENTICATION_BACKENDS`
4. Include `guest_user.urls` in your URLs
5. Decorate your views with `@allow_guest_user`:

   ```python
   from guest_user.decorators import allow_guest_user

   @allow_guest_user
   def my_view(request):
       assert request.user.is_authenticated
       return render(request, "my_view.html")
   ```

A more detailed guide is available in the
[installation documentation](https://django-guest-user.readthedocs.io/en/latest/setup.html#how-to-install).

## Contributing

All contributions are welcome! Please read the
[contributing guidelines](CONTRIBUTING.md) in this repostory.

## Development Status

This project is under active development. Thanks to
[previous work](https://github.com/danfairs/django-lazysignup) the core
functionality is well-established and this package builds on top of it.

This project was created because the original project has been in an inactive
state without major updates in a long time. The code base was rewritten with
only modern versions of Python and Django in mind.
