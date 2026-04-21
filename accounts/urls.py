from django.urls import path
from . import views

# URL patterns for login, logout and account setup
urlpatterns = [
    path("staff/register/", views.staff_register, name="StaffRegister"),
    path("login/", views.login, name="Login"),
    path("logout/", views.logout_view, name="Logout"),
    path("player/set-password/", views.player_set_password, name="PlayerSetPassword"),
]
