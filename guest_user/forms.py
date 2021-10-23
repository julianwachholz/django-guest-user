from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm


class UserCreationForm(BaseUserCreationForm):
    def get_credentials(self):
        return {
            "username": self.cleaned_data["username"],
            "password": self.cleaned_data["password1"],
        }
