How to use
==========

Allowing guests
---------------

Guest users are not created by default for every unauthenticated request.
Instead, the :func:`@allow_guest_user<guest_user.decorators.allow_guest_user>`
decorator or :class:`AllowGuestUserMixin<guest_user.mixins.AllowGuestUserMixin>`
is used to tell Django explicitly which views may create a new temporary guest.

.. code:: python

  from guest_user.decorators import allow_guest_user

  @allow_guest_user
  def hello_guest(request):
      """
      This view will always have an authenticated user, but some may be guests.
      The default username generator will create a UUID4.

      Example response: "Hello, b5daf1dd-1a2f-4d18-a74c-f13bf2f086f7!"
      """
      return HttpResponse(f"Hello, {request.user.username}!")

Each time an anonymous user requests a decorated view, a new temporary guest
user will be created and logged in with a randomly generated username. The
username generator can be defined using the
:attr:`GUEST_USER_NAME_GENERATOR<guest_user.app_settings.AppSettings.NAME_GENERATOR>` setting.

Converting guests
-----------------

At any point in time, the guest user may choose to permanently register with the
website by using the conversion view. This will delete the associated Guest
model instance for the user and prevent deletion from cleanup jobs.

Given your existing project with a link to a registration page, you can add use
the provided :func:`is_guest_user<guest_user.templatetags.guest_user.is_guest_user>`
template filter to check if the current user is a guest and link to the conversion
page respectively.

.. code:: jinja

  {% load guest_user %}

  {% if user|is_guest_user %}
    {# user is a guest instance, link to conversion page #}
    <a href="{% url "guest_user_convert" %}">Sign up and save your work!</a>
  {% else %}
    {# regular sign up link #}
    <a href="/register/">Register now!</a>
  {% endif %}

The default form is a subclass of Django's UserCreationForm with the addition
of a :meth:`get_credentials()<guest_user.forms.UserCreationForm.get_credentials>`
method required to sign the user in after converting.

If your sign up process requires additional data, you can change the form with the
:attr:`GUEST_USER_CONVERT_FORM<guest_user.app_settings.AppSettings.CONVERT_FORM>` setting.
You will likely want to overwrite the template used to display the form at
``guest_user/convert_form.html`` as well.

Once a user completes the conversion step, they will be redirected to the success
view which shows the ``guest_user/convert_success.html`` template. You can overwrite
the success url by setting
:attr:`GUEST_USER_CONVERT_REDIRECT_URL<guest_user.app_settings.AppSettings.CONVERT_REDIRECT_URL>`.

Restricting access
------------------

While ``django-guest-user`` makes it very easy for visitors to start using your
site, there may still be parts of it that should not be accessible to guests.
Two additional :mod:`decorators<guest_user.decorators>` or :mod:`mixins<guest_user.mixins>`
can be used to restrict access to either regular users or guests only.

.. code:: python

  from guest_user.decorators import guest_user_required
  from guest_user.mixins import RegularUserRequiredMixin

  @guest_user_required
  def why_convert(request):
      """Show reasons why to convert, only for guest users."""
      return TemplateResponse("reasons_to_convert.html")

  class SettingsView(RegularUserRequiredMixin, FormView):
      """Only allow registered users to change their settings."""
      form_class = SettingsForm

Cleaning up
-----------

Because the user sessions have a limited lifetime, guest users need to be cleaned
up at regular intervals to prevent filling up the database with users and related
objects that cannot be accessed anymore.

This can be done manually in the admin, by selecting the
`"Delete selected guests older than ..."` action, or by running the management
command ``delete_expired_users`` on a schedule (for example using a cronjob)::

  ./manage.py delete_expired_users

These methods will remove any Guest users that have a created_at date older than
the :attr:`GUEST_USER_MAX_AGE<guest_user.app_settings.AppSettings.MAX_AGE>` setting.
By default this is the same duration as the Django session cookie.

.. note::

  To prevent exceptions or data integrity errors, each foreign key to your User
  model should have ``on_delete`` set to ``CASCADE`` or ``SET_NULL``.

Customizing
-----------

This package provides a number of :doc:`settings<config>` to customize the
behaviour of guest user creation and conversion. This section will show how to
use different options to better fit your specific requirements.

Temporary usernames
~~~~~~~~~~~~~~~~~~~

To generate temporary usernames for your guests that you can also show in your
templates, you can override the function used to generate the username by setting
:attr:`GUEST_USER_NAME_GENERATOR<guest_user.app_settings.AppSettings.NAME_GENERATOR>`
to an import string of a custom function or use one of the provided generators.
