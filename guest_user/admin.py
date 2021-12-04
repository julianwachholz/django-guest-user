from datetime import timedelta

from django.contrib import admin

from . import settings
from .functions import get_guest_model
from .models import Guest


class GuestAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "is_expired"]
    actions = ["delete_expired_guests"]
    fields = ["user", "created_at"]
    readonly_fields = ["user", "created_at", "is_expired"]

    def is_expired(self, obj):
        return obj.is_expired()

    is_expired.boolean = True

    def delete_expired_guests(self, request, queryset):
        expired_guests = queryset.filter_expired()
        count = expired_guests.count()

        for guest in expired_guests:
            # Call delete method to trigger signals and cascades
            guest.user.delete()

        self.message_user(request, f"Deleted {count} guests.")

    delete_expired_guests.short_description = (
        "Delete selected guests older than {}".format(
            timedelta(seconds=settings.MAX_AGE)
        )
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_deleted_objects(self, objs, request):
        """
        Show the correct CASCADE for guest deletion.

        This Guest admin's DELETE actions will always try to delete the associated
        user objects instead of the guest instances, to allow a full cascade.

        """
        user_objs = [obj.user for obj in objs]
        return super().get_deleted_objects(user_objs, request)

    def delete_model(self, request, obj):
        """
        Make the delete action cascade.

        """
        obj.user.delete()

    def delete_queryset(self, request, queryset):
        """
        Make the delete action cascade.

        """
        for obj in queryset:
            obj.user.delete()


if get_guest_model() == Guest:
    admin.site.register(Guest, GuestAdmin)
