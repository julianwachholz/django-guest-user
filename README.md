[![Code Lint](https://github.com/julianwachholz/django-guest-user/actions/workflows/lint.yml/badge.svg)](https://github.com/julianwachholz/django-guest-user/actions/workflows/lint.yml)
[![Python Tests](https://github.com/julianwachholz/django-guest-user/actions/workflows/test.yml/badge.svg)](https://github.com/julianwachholz/django-guest-user/actions/workflows/test.yml)
[![Documentation](https://readthedocs.org/projects/django-guest-user/badge/?style=flat)](https://django-guest-user.readthedocs.io)

# django-guest-user

A Django app that allows visitors to interact with your site as a guest user
without requiring registration.

Largely inspired by [django-lazysignup](https://github.com/danfairs/django-lazysignup) and rewritten for Django 3.1+ and Python 3.7+.

Find the [**complete documentation**](https://django-guest-user.readthedocs.io/)
on Read the Docs.

## Quickstart

1. Install the `django-guest-user` package
2. Add `guest_user` to your `INSTALLED_APPS` and migrate your database
3. Add `guest_user.backends.GuestBackend` to your `AUTHENTICATION_BACKENDS`
4. Include `guest_user.urls` in your URLs
5. Decorate your views with `@allow_guest_user`:

   ```
   from guest_user.decorators import allow_guest_user

   @allow_guest_user
   def my_view(request):
       assert request.user.is_authenticated
       return render(request, "my_view.html")
   ```

## Status

This project is still under development. But thanks to [previous work](https://github.com/danfairs/django-lazysignup) it is largely functional.

I decided to rewrite the project since the original project hasn't seen any
larger updates for a few years now. The initial code base was written a long
time ago as well.
