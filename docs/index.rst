django-guest-user
=================

.. image:: https://github.com/julianwachholz/django-guest-user/actions/workflows/lint.yml/badge.svg
   :target: https://github.com/julianwachholz/django-guest-user/actions/workflows/lint.yml
   :alt: Code Lint

.. image:: https://github.com/julianwachholz/django-guest-user/actions/workflows/test.yml/badge.svg
   :target: https://github.com/julianwachholz/django-guest-user/actions/workflows/test.yml
   :alt: Python Tests

A reusable `Django`_ app that allows site visitors to interact with your project
as if they were registered users without having to sign up first.

.. _Django: https://www.djangoproject.com/

Anonymous visitors who request a decorated page get a real temporary user object
assigned and are logged in automatically.

By allowing these guests to use all features of your page, the barrier to entry
is lowered and conversion rates for new users can increase. Visitors will
be more invested in your service and more likely to convert if they already made
progress and created content using your application.

Converting to a permanent user takes very few clicks and allows visitors to save
their progress and don't risk to lose it once the guest users are cleaned up.

This project was largely inspired by `django-lazysignup`_ and rewritten for
modern Django and Python versions.

.. _django-lazysignup: https://github.com/danfairs/django-lazysignup

Quick links
-----------

- `PyPI Package <https://pypi.org/project/django-guest-user/>`_
- `GitHub Repository <https://github.com/julianwachholz/django-guest-user>`_
- `5 Steps Quickstart <https://github.com/julianwachholz/django-guest-user#quickstart>`_
- `How to Contribute <https://github.com/julianwachholz/django-guest-user/blob/main/CONTRIBUTING.md>`_

.. toctree::
   :maxdepth: 2
   :caption: Documentation

   setup
   usage
   contrib
   advanced
   config
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
