from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from accounts.models import Staff, Player
from accounts.decorators import staff_required
from django.shortcuts import render, redirect
from .forms import PlayerForm, PlayerUserForm

# @login required makes sure that you can only access this confidential page if you are signed in - prevents unauthorised access
@login_required
@staff_required
def staff_players_hub(request):
    player_form = PlayerForm()
    user_form = PlayerUserForm()

    if request.method == "POST":

        # CREATE PLAYER
        if "first_name" in request.POST:
            player_form = PlayerForm(request.POST)
            user_form = PlayerUserForm(request.POST)

            if player_form.is_valid() and user_form.is_valid():

                # Duplicate check to avoid adding the same player twice
                if Player.objects.filter(
                    first_name=player_form.cleaned_data["first_name"],
                    last_name=player_form.cleaned_data["last_name"],
                    date_of_birth=player_form.cleaned_data["date_of_birth"]
                ).exists():
                    messages.error(request, "This player already exists")

                # Check the username is not already taken
                elif User.objects.filter(username=user_form.cleaned_data["username"]).exists():
                    messages.error(request, "That username is already taken")

                else:
                    # Create the user account then link it to the player
                    user = User.objects.create_user(
                        username=user_form.cleaned_data["username"],
                        password=user_form.cleaned_data["password"]
                    )
                    player = player_form.save(commit=False)
                    player.user = user
                    player.save()

                    messages.success(request, "Player created successfully!")
                    return redirect("StaffPlayersHub")

        # DELETE PLAYER
        elif "deletePlayerID" in request.POST:
            player_id = request.POST.get("deletePlayerID")
            player = Player.objects.get(id=player_id)
            if player.user:
                player.user.delete()  # CASCADE deletes the Player too
            else:
                player.delete()
            messages.success(request, "Player deleted")
            return redirect("StaffPlayersHub")

    # Order by player ID
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    players = Player.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(position__icontains=q)
    ).order_by("id")
    return render(request, "staff_players_hub.html", {
        "players": players,
        "player_form": player_form,
        "user_form": user_form,
        "q": q
    })


 # UPDATE PLAYER
@login_required
@staff_required
def update_player(request, player_id):

    player = Player.objects.get(id=player_id)

    if request.method == "POST":
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            messages.success(request, "Player updated successfully!")
            return redirect("StaffPlayersHub")
    else:
        form = PlayerForm(instance=player)

    return render(request, "update_player.html", {"player": player, "form": form})
