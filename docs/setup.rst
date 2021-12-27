Dependencies
============

This project is thoroughly tested on these setups:

- Python 3.7, 3.8, 3.9 and 3.10
- Django 3.2, 4.0 and the main branch

In addition, your Django project should be using :doc:`django:ref/contrib/auth`.

How to install
==============

Install the package from PyPI with your favorite package manager::

   pip install django-guest-user
   # or simiar, e.g.
   poetry add django-guest-user

Add the app to your :ref:`django:ref/settings:``installed_apps```
and :ref:`django:ref/settings:``authentication_backends```::

   # settings.py
   INSTALLED_APPS = [
      # ... other apps
      "guest_user",
   ]

   AUTHENTICATION_BACKENDS = [
      "django.contrib.auth.backends.ModelBackend",
      # it should be the last entry to prevent unauthorized access
      "guest_user.backends.GuestBackend",
   ]

Allow guests to convert to registered users by adding the URLs to your :doc:`URLconf<django:topics/http/urls>`::

   # urls.py
   urlpatterns = [
      # ... other patterns
      path("convert/", include("guest_user.urls")),
   ]

Last but not least, prepare the guest user table by running migrations::

    python manage.py migrate


Migrating from ``django-lazysignup``
````````````````````````````````````

``django-guest-user`` can be used a a drop-in replacement for `django-lazysignup`_.

.. _django-lazysignup: https://github.com/danfairs/django-lazysignup

Given the temporary nature of guest or lazy users, the packages can be replaced
without breaking the functionality of any existing (non-temporary) users.

.. note::

   By uninstalling lazysignup, any current temporary users will lose their
   associated data and be signed out of their session.

The following decorators and template filters need to be replaced by their respective counterparts.

- ``@allow_lazy_user`` ➡️ :func:`@allow_guest_user<guest_user.decorators.allow_guest_user>`
- ``@require_lazy_user`` ➡️ :func:`@guest_user_required<guest_user.decorators.guest_user_required>`
- ``@require_nonlazy_user`` ➡️ :func:`@regular_user_required<guest_user.decorators.regular_user_required>`
- Template filter ``is_lazy_user`` ➡️ :func:`is_guest_user<guest_user.templatetags.guest_user.is_guest_user>`
