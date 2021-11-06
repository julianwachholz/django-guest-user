from django.conf import settings as django_settings
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login
from django.shortcuts import redirect, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.module_loading import import_string
from django.views.generic import FormView, TemplateView

from . import settings
from .exceptions import NotGuestError
from .functions import get_guest_model, is_guest_user


class ConvertFormView(FormView):
    """
    Allow a guest to convert to a regular user.

    """

    anonymous_redirect = None
    user_redirect = None

    success_url = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "guest_user/convert_form.html"

    success_url_allowed_hosts = set()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect(self.get_anonymous_redirect())

        if not is_guest_user(request.user):
            return redirect(self.get_user_redirect())

        return super().dispatch(request, *args, **kwargs)

    def get_anonymous_redirect(self):
        """Return the URL to redirect anonymous users to."""
        return self.anonymous_redirect or django_settings.LOGIN_URL

    def get_user_redirect(self):
        """Return the URL to redirect regular users to."""
        return self.user_redirect or django_settings.LOGIN_REDIRECT_URL

    def get_form_class(self):
        return self.form_class or import_string(settings.CONVERT_FORM)

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        initial = super().get_initial()
        if settings.CONVERT_PREFILL_USERNAME:
            initial["username"] = self.request.user.username
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "POST":
            kwargs["instance"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({self.redirect_field_name: self.get_redirect_url()})
        return context

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        GuestModel = get_guest_model()

        try:
            GuestModel.objects.convert(form)
        except NotGuestError:
            # Redirect if it's already a regular user.
            pass
        else:
            # Authenticate the user with standard backend.
            login(self.request, authenticate(self.request, **form.get_credentials()))

        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.get_redirect_url() or self.get_default_redirect_url()

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name, self.request.GET.get(self.redirect_field_name, "")
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        return resolve_url(self.success_url or settings.CONVERT_REDIRECT_URL)


convert_form = ConvertFormView.as_view()


class ConvertSuccessView(TemplateView):
    template_name = "guest_user/convert_success.html"


convert_success = ConvertSuccessView.as_view()
