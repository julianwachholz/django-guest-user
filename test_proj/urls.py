from django.urls import include, path

from . import views

urlpatterns = [
    path("allow_guest_user/", views.allow_guest_user_view),
    path("guest_user_required/", views.guest_user_required_view),
    path("regular_user_required/", views.regular_user_required_view),
    path("convert/", include("guest_user.urls")),
]
