import django.dispatch

guest_created = django.dispatch.Signal()
"""
A guest account has been created for a visitor.

:param user: The new guest user.
:param request: The request that created the guest user.

"""

converted = django.dispatch.Signal()
"""
A guest user converted to a regular registered user.

:param user: The now registered user.

"""
