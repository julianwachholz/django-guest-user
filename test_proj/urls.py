from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Function view decorators
    path("allow_guest_user/", views.allow_guest_user_view),
    path("guest_user_required/", views.guest_user_required_view),
    path("regular_user_required/", views.regular_user_required_view),
    # Class based views with mixins
    path("mixin/allow_guest_user/", views.AllowGuestUserView.as_view()),
    path("mixin/guest_user_required/", views.GuestUserRequiredView.as_view()),
    path("mixin/regular_user_required/", views.RegularUserRequiredView.as_view()),
    # Conversion view
    path("convert/", include("guest_user.urls")),
]
