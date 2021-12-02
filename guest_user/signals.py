from django.dispatch import Signal

guest_created = Signal()
"""
A visitor accessed a view that created a guest user.

:param user: The new guest user.
:param request: The request that created the guest user.

"""

converted = Signal()
"""
A guest user converted to a regular registered user.

:param user: The now registered user.

"""
