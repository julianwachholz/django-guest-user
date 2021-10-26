from django.db import models
from guest_user.models import Guest


class CustomGuest(Guest):
    """Custom guest model."""

    extra_data = models.CharField(max_length=255, blank=True, default="dummy")
