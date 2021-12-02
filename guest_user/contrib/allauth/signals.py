from django.core.exceptions import ValidationError
from django.dispatch import Signal, receiver

from allauth.socialaccount.signals import social_account_added

from ...functions import get_guest_model, is_guest_user


@receiver(social_account_added)
def convert_guest_with_social_login(sender, request, sociallogin, **kwargs):
    """
    Check if a guest user has added a social account.

    When a user logged in using a social account, the guest is converted.

    We will also ensure that the social account's username is used.

    """
    user = request.user

    if is_guest_user(user):
        # Convert the user right away, since the social account
        # has already been connected at this point.
        get_guest_model().objects.filter(user=user).delete()

        from allauth.account.adapter import get_adapter as get_account_adapter
        from allauth.socialaccount.adapter import get_adapter as get_social_adapter

        # Normally, allauth will only populate a user that registers using a social account,
        # but in this case the user already exists, so we need to populate it ourselves.
        social_adapter = get_social_adapter()
        social_adapter.populate_user(
            request,
            sociallogin,
            sociallogin.account.get_provider().extract_common_fields(
                sociallogin.account.extra_data
            ),
        )
        account_adapter = get_account_adapter()
        try:
            username = getattr(user, user.USERNAME_FIELD)
            account_adapter.clean_username(username)
        except ValidationError:
            # Empty the invalid username to allow fallbacks in `populate_username`
            setattr(user, user.USERNAME_FIELD, "")
        account_adapter.populate_username(request, user)
        user.save()

        converted_social_account.send(sender=sender, user=user, sociallogin=sociallogin)


converted_social_account = Signal()
"""
A guest user converted by connecting a social account.

:param user: The converted user object.
:param sociallogin: The social login object that converted the guest.

"""
