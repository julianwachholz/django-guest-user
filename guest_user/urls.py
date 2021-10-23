from django.urls import path

from .views import convert_form, convert_success

urlpatterns = [
    path("", convert_form, name="guest_user_convert"),
    path("success/", convert_success, name="guest_user_convert_success"),
]
