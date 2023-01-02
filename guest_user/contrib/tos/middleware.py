from tos.middleware import UserAgreementMiddleware
from guest_user.functions import is_guest_user


class GuestUserAgreementMiddleware(UserAgreementMiddleware):
    def should_fast_skip(self, request):
        if super().should_fast_skip(request):
            return True
        return is_guest_user(request.user)
