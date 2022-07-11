from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest
from django.shortcuts import redirect


class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, _("You are not authorized! Log in, please.")
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnershipRequiredMixin:
    """Verify that the current user is owner of affected object."""

    model_user_id_field_name = 'user_id'
    failure_message = ""
    failure_url = None

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        object_ = self.model.objects.get(pk=self.kwargs.get('pk'))
        if getattr(object_, self.model_user_id_field_name) == request.user.id:
            return super().dispatch(request, *args, **kwargs)
        if self.failure_message:
            messages.error(request, self.failure_message)
        failure_url = self.get_failure_url()
        return redirect(failure_url)

    def get_failure_url(self):
        if self.failure_url:
            return self.failure_url
        raise ImproperlyConfigured("No URL to redirect to. Provide a failure_url.")
