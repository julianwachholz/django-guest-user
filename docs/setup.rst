Dependencies
============

This project is thoroughly tested on these setups:

- Python 3.7, 3.8 and 3.9
- Django 3.1, 3.2 and the main branch (4.0)

In addition, your Django project must be using ``django.contrib.auth``.

How to install
==============

Install the package from PyPI with your favorite package manager::

   pip install django-guest-user
   # or simiar, e.g.
   poetry add django-guest-user

Add the app to your ``INSTALLED_APPS`` and ``AUTHENTICATION_BACKENDS``::

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

Allow guests to convert to registered users by adding the URLs::

   # urls.py
   urlpatterns = [
      # ... other patterns
      path("convert/", include("guest_user.urls")),
   ]

Last but not least, prepare the guest user table by running migrations::

    python manage.py migrate
