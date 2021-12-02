API
===


Decorators
----------

.. currentmodule:: guest_user.decorators

.. automodule:: guest_user.decorators

.. autodecorator:: allow_guest_user

.. autodecorator:: guest_user_required

.. autodecorator:: regular_user_required


Mixins
------

.. automodule:: guest_user.mixins
   :members:

Template Tags
-------------

The package registers a template filter to use in your Django templates.

.. autodata:: guest_user.templatetags.guest_user.is_guest_user
   :no-value:

Functions
---------

Several helper functions are provided for advanced usage.

.. automodule:: guest_user.functions
   :members:

Signals
-------

.. automodule:: guest_user.signals
   :members:
