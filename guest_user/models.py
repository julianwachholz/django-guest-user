from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.module_loading import import_string

from . import settings
from .exceptions import NotGuestError
from .functions import is_guest_user
from .signals import converted

User = get_user_model()


class GuestManager(models.Manager):
    def create_guest_user(self):
        """
        Create a guest user.

        Returns the underlying User object.

        """
        generate_username = import_string(settings.NAME_GENERATOR)
        user = User.objects.create_user(generate_username(), "")
        self.create(user=user)
        return user

    def convert(self, form):
        """
        Convert a guest user to a regular one.

        The form passed in is expected to be a ModelForm instance,
        bound to the user to be converted.

        The converted ``User`` object is returned.
        Raises a TypeError if the user is not a temporary guest.

        """
        if not is_guest_user(form.instance):
            raise NotGuestError("You cannot convert a non guest user")

        user = form.save()

        # We need to remove the Guest instance assocated with the
        # newly-converted user
        self.filter(user=user).delete()
        converted.send(self, user=user)
        return user


class Guest(models.Model):
    """A temporary guest user."""

    user = models.OneToOneField(
        to=django_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="guest+",
    )

    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
        db_index=True,
    )

    objects = GuestManager()

    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"
        swappable = "GUEST_USER_MODEL"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.user)
