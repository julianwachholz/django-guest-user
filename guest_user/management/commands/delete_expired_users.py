from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from ... import settings
from ...models import Guest


class Command(BaseCommand):
    help = "Delete expired guest users."

    def handle(self, **options):
        """Delete every user"""
        delete_before = now() - timedelta(seconds=settings.MAX_AGE)
        guests = Guest.objects.filter(
            user__last_login__lt=delete_before,
        ).select_related("user")

        for guest in guests:
            guest.user.delete()
