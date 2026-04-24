from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from .forms import StaffRegisterForm
from .models import Staff, Player
from .decorators import player_required
from django.shortcuts import redirect
from django.contrib.auth import logout


# Create your views here.

# Staff registration page for creating staff logins
def staff_register(request):
    if request.method == "POST":
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['access_code'] != settings.STAFF_ACCESS_CODE:
                messages.error(request, "Invalid access code")
                return render(request, "staff_register.html", {"form": form})

            user = form.save()
            Staff.objects.create(user=user)
            messages.success(request, "Account created successfully!")
            return redirect("StaffRegister")
    else:
        form = StaffRegisterForm()

    return render(request, "staff_register.html", {"form": form})


 # Shared login page for both staff and players
@ratelimit(key='ip', rate='5/m', method='POST', block=False)
def login(request):
    if getattr(request, 'limited', False):
        messages.error(request, "Too many login attempts. Please wait a minute and try again.")
        return redirect("Login")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        auth_login(request, user)

        if Staff.objects.filter(user=user).exists():
            return redirect("StaffHomepage")

        if Player.objects.filter(user=user).exists():
            player = Player.objects.get(user=user)
            if player.must_change_password:
                return redirect("PlayerSetPassword")
            return redirect("PlayerHomepage")

        return redirect("LandingPage")

    return render(request, "login.html", {"form": form})


# Logs the user out and sends them back to the landing page
def logout_view(request):
    logout(request)
    return redirect("LandingPage")


# Forces players to change their password on first login
@login_required
@player_required
def player_set_password(request):
    form = PasswordChangeForm(request.user, request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)

        player = Player.objects.get(user=request.user)
        player.must_change_password = False
        player.save()

        messages.success(request, "Password updated. Welcome to Ekota!")
        return redirect("PlayerHomepage")

    return render(request, "player_set_password.html", {"form": form})
