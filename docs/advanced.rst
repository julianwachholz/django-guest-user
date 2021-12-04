Advanced usage
==============

Swappable Guest model
---------------------

If you want to add additional fields to your temporary guests, you can swap out
the Guest model with your own by customizing the
:attr:`GUEST_USER_MODEL<guest_user.app_settings.AppSettings.MODEL>` setting.

This example overrides the guest model with a custom model to override the
manager and the logic on how to create a user, which can be useful if you do not
use the :doc:`django:ref/contrib/auth` app.

.. code:: python

    # settings.py
    GUEST_USER_MODEL = "my_app.MyGuest"

    # my_app/models.py
    from guest_user.models import Guest, GuestManager

    class MyGuestManager(GuestManager):
        def create_guest_user(self, request=None, username=None):
            # Override how to create a new User instance
            user = MyUserModel.objects.create(username=username)
            return user

    class MyGuest(Guest):
        objects = MyGuestManager()
