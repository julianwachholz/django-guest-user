from django.core.management.base import BaseCommand

from ...functions import get_guest_model


class Command(BaseCommand):
    help = "Delete expired guest users."

    def handle(self, **options):
        """Delete every user"""
        GuestModel = get_guest_model()
        GuestModel.objects.delete_expired()
