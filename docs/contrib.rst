Integrations
============

django-allauth
--------------

`django-allauth`_ allows users to register with a multitude of third party providers
such as Twitter, Apple, Google, etc.

.. _django-allauth: https://allauth.org/

This module registers a signal handler that will allow automatically converting
guest users when they decide to connect a social media account.
The user's social media account username will be used as their username.

Should the username from the connected social account be already taken,
a random numeric suffix will be appended. For example, if "Rufus" is already taken,
the new user will get the username "Rufus3". This suggests allowing users to
change their username later when desired.

Setup
~~~~~

This submodule is not enabled by default. To enable it, add it to your ``INSTALLED_APPS``.

.. code:: python

  INSTALLED_APPS = [
      "allauth",
      "allauth.account",
      "allauth.socialaccount",
      # ...
      "guest_user",
      "guest_user.contrib.allauth",
  ]

Usage
~~~~~

In your convert page template, you can integrate the social account login.

.. code:: jinja

  {% load guest_user %}

  {% include "socialaccount/snippets/provider_list.html" with process=user|is_guest_user|yesno:"connect,login" %}

If you use the same inclusion tag for signup and login, make sure that the process
argument is set to connect for guest users, as seen above.

Signals
~~~~~~~

You may connect an additional signal that is called when a guest user converted
by connecting a social account.

.. autodata:: guest_user.contrib.allauth.signals.converted_social_account
  :annotation: = Signal(user, sociallogin)

As an example, this handler will save the avatar URL.

.. code:: python

  @receiver(converted_social_account)
  def social_converted(sender, user, sociallogin, **kwargs):
      """Save the avatar URL to the profile."""
      avatar_url = sociallogin.account.get_avatar_url()
      if avatar_url:
          profile = user.profile
          profile.avatar_url = avatar_url
          profile.save()


django-tos
----------

`Django-TOS`_ allows sites to force users to explicitly agree to each revision of
the site's terms of service.

.. _django-tos: https://github.com/revsys/django-tos/

Django-TOS can do this one of two ways - (1) only when a user logs in, and (2) on
each request by each user, implemented with a Django middleware. Django-guest-users
does not interfere with option (1), but it does interfere with option (2).

.. note::
   This module is not necessary if you use option (1), but is helpful if you use
   option (2).

This module provides a custom middleware that allows Django-TOS to skip the TOS
check for guest users (eg: those users who have an auto-generated guest user account,
but do not have an explicit user account).

Setup
~~~~~

Install and configure django-tos with option (2), but instead of adding
``tos.middleware.UserAgreementMiddleware`` to ``MIDDLEWARE`` in your project's
``settings.py``, add
``guest_user.contrib.tos.middleware.GuestUserAgreementMiddleware``.
