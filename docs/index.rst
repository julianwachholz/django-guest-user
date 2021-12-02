django-guest-user
=================

A reusable Django app that allows site visitors to interact with your Django
project as if they were registered users without having to sign up first.

By allowing anonymous guests to use all features of your page, the barrier to
entry is lowered and conversion rates for new users can increase. Converting
a guest user takes a few clicks and allows visitors to save their progress
and don't risk to lose it once the guest users are cleaned up.

This project was largely inspired by `django-lazysignup`_ and rewritten for
modern Django and Python versions.

.. _django-lazysignup: https://github.com/danfairs/django-lazysignup

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   setup
   usage
   contrib
   config
   api

Quickstart
==========

1. Install the ``django-guest-user`` package
2. Add ``guest_user`` to your ``INSTALLED_APPS`` and migrate your database
3. Add ``guest_user.backends.GuestBackend`` to your ``AUTHENTICATION_BACKENDS``
4. Include ``guest_user.urls`` in your URLs
5. Decorate your views with ``@allow_guest_user``::

      from guest_user.decorators import allow_guest_user

      @allow_guest_user
      def my_view(request):
          assert request.user.is_authenticated
          return render(request, "my_view.html")

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
