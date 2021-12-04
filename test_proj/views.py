from django.shortcuts import render
from django.views.generic import View
from guest_user.decorators import (
    allow_guest_user,
    guest_user_required,
    regular_user_required,
)
from guest_user.mixins import (
    AllowGuestUserMixin,
    GuestUserRequiredMixin,
    RegularUserRequiredMixin,
)


@allow_guest_user()
def allow_guest_user_view(request):
    return render(request, "guest.html")


class AllowGuestUserView(AllowGuestUserMixin, View):
    def get(self, request):
        return render(request, "guest.html")


@guest_user_required()
def guest_user_required_view(request):
    return render(request, "guest.html")


class GuestUserRequiredView(GuestUserRequiredMixin, View):
    def get(self, request):
        return render(request, "guest.html")


@regular_user_required()
def regular_user_required_view(request):
    return render(request, "guest.html")


class RegularUserRequiredView(RegularUserRequiredMixin, View):
    def get(self, request):
        return render(request, "guest.html")
