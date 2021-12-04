from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm


class UserCreationForm(BaseUserCreationForm):
    """
    A modelform that creates a standard Django user.

    Custom implementations must implement :meth:`get_credentials`.

    """

    def get_credentials(self) -> dict:
        """
        Get the credentials required to log the user in after conversion.

        The credentials are passed to Django's :func:`authenticate()<django.contrib.auth.authenticate>`.

        :return: Login credentials. This is usually a dict with "username" and "password".

        """
        return {
            "username": self.cleaned_data["username"],
            "password": self.cleaned_data["password1"],
        }
