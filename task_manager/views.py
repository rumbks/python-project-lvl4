from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    success_message = _("You are logged in")
    template_name = 'login.html'
    next_page = 'main'


class LogoutView(auth_views.LogoutView):
    next_page = 'main'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
