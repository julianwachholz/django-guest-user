from django.template import Library

from ..functions import is_guest_user as is_guest_user_func

register = Library()

is_guest_user = register.filter(is_guest_user_func)
