from datetime import timedelta

from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError, models, transaction
from django.forms import ModelForm
from django.utils.module_loading import import_string
from django.utils.timezone import now

from . import settings
from .exceptions import NotGuestError
from .functions import is_guest_user
from .signals import converted, guest_created

UserModel = get_user_model()


class GuestQuerySet(models.QuerySet):
    def filter_expired(self):
        delete_before = now() - timedelta(seconds=settings.MAX_AGE)
        return self.filter(
            created_at__lt=delete_before,
        ).select_related("user")


class GuestManager(models.Manager.from_queryset(GuestQuerySet)):
    """
    Manager for Guest objects.

    """

    @property
    def generate_username(self):
        return import_string(settings.NAME_GENERATOR)

    def create_guest_user(self, request=None, username: str = None) -> UserModel:
        """
        Create a guest user.

        Returns the underlying User object.

        :param request: The current request object.
        :param username: The preferred username for the user, may be None.

        """
        if username is None:
            username = self.generate_username()

        user = None
        while user is None:
            try:
                with transaction.atomic():
                    user = UserModel.objects.create_user(username, "")
            except IntegrityError:
                # retry with a new username
                username = self.generate_username()

        self.create(user=user)
        if request is not None:
            guest_created.send(self, user=user, request=request)
        return user

    def convert(self, form: ModelForm) -> UserModel:
        """
        Convert a guest user to a regular one.

        The form passed in is expected to be a ModelForm instance,
        bound to the user to be converted.

        :raises: TypeError if the user is not a temporary guest.
        :param form: The model form used to create the permanent user.
        :returns: The converted ``User`` object.

        """
        if not is_guest_user(form.instance):
            raise NotGuestError("You cannot convert a non guest user")

        user = form.save()

        # We need to remove the Guest instance assocated with the
        # newly-converted user
        self.filter(user=user).delete()
        converted.send(self, user=user)
        return user

    def delete_expired(self):
        """
        Delete all expired guest users.

        """
        for guest in self.filter_expired():
            # Call delete method to trigger signals and cascades
            guest.user.delete()


class Guest(models.Model):
    """
    A temporary guest user.

    Users linked to a Guest instance are considered temporary guests and will
    be deleted by cleanup jobs after their expiration.

    The age of a guest user is determined by the ``created_at`` field.

    This model is swappable with the :attr:`GUEST_USER_MODEL<guest_user.app_settings.AppSettings.MODEL>` setting.
    Custom Guest models should use the GuestManager or a custom manager that
    implements the same custom methods.

    """

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

    def is_expired(self) -> bool:
        """
        Check if the guest user has expired.

        """
        return self.created_at < now() - timedelta(seconds=settings.MAX_AGE)
