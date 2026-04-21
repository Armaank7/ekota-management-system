from django.contrib.auth.decorators import user_passes_test

from .models import Staff, Player


# Checks if the logged in user has a staff account linked to them
def staff_required(view_func):
    check_staff = user_passes_test(
        lambda user: Staff.objects.filter(user=user).exists(),
        login_url="/",
        redirect_field_name=None,
    )
    return check_staff(view_func)


# Checks if the logged in user has a player account linked to them
def player_required(view_func):
    check_player = user_passes_test(
        lambda user: Player.objects.filter(user=user).exists(),
        login_url="/",
        redirect_field_name=None,
    )
    return check_player(view_func)
