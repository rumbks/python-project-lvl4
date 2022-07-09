from django.contrib.auth import views as auth_views


class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    next_page = 'main'


class LogoutView(auth_views.LogoutView):
    next_page = 'main'
