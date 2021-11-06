# guest_user.contrib.allauth

This small module will integrate `django-allauth` with `django-guest-user`.

It will automatically convert guest users that sign up using a social account
and register with their social account username.

Should the username from the connected social account be already taken,
a numeric suffix will be appeneded.

## Requirements

- [django-allauth](https://www.intenct.nl/projects/django-allauth/)

## Installation

Add the contrib package to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # ...
    "guest_user",
    "guest_user.contrib.allauth",
]
```

### Signals

Module: `guest_user.contrib.allauth.signals`

#### `converted_social_account(user, sociallogin)`

You may connect an additional signal that is called when a guest user converted by
connecting a social account. For example, this handler will save the avatar URL:

```python
@receiver(converted_social_account)
def social_converted(sender, user, sociallogin, **kwargs):
    """Save the avatar URL to the profile."""
    avatar_url = sociallogin.account.get_avatar_url()
    if avatar_url:
        profile = user.profile
        profile.avatar_url = avatar_url
        profile.save()
```
