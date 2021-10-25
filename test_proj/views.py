from django.shortcuts import render
from guest_user.decorators import (
    allow_guest_user,
    guest_user_required,
    regular_user_required,
)


@allow_guest_user
def allow_guest_user_view(request):
    return render(request, "dummy.html")


@guest_user_required
def guest_user_required_view(request):
    return render(request, "dummy.html")


@regular_user_required
def regular_user_required_view(request):
    return render(request, "dummy.html")
