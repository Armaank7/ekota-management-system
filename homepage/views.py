from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from accounts.models import Player
from accounts.decorators import staff_required, player_required
from matches.models import Match, MatchAppearance
from training.models import Training, TrainingAttendance
from .forms import StaffProfileForm, PlayerProfileForm

# Create your views here.

# Landing page shown before login
def landing_page(request):
    return render(request, "landing.html")


# Staff dashboard page
@login_required
@staff_required
def staff_homepage(request):
    return render(request, "staff_homepage.html")


# Lets staff update their own user details
@login_required
@staff_required
def staff_profile(request):
    if request.method == "POST":
        form = StaffProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("StaffProfile")
    else:
        form = StaffProfileForm(instance=request.user)

    return render(request, "staff_profile.html", {"form": form})


# Player dashboard page
@login_required
@player_required
def player_homepage(request):
    return render(request, "player_homepage.html")


# Shows players the match list in read only form
@login_required
@player_required
def player_match_fixtures(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    matches = Match.objects.filter(
        Q(opponent_name__icontains=q) | Q(match_type__icontains=q) | Q(venue_type__icontains=q)
    ).order_by("match_date")
    return render(request, "player_match_fixtures.html", {"matches": matches, "q": q})


# Shows players the training list in read only form
@login_required
@player_required
def player_training_sessions(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    sessions = Training.objects.filter(
        Q(training_type__icontains=q) | Q(notes__icontains=q)
    ).order_by("training_date")
    return render(request, "player_training_sessions.html", {"sessions": sessions, "q": q})


# Shows each player their own match and training summary
@login_required
@player_required
def player_performance(request):
    player = Player.objects.get(user=request.user)
    appearances = MatchAppearance.objects.filter(player=player).order_by("match__match_date")
    attendance = TrainingAttendance.objects.filter(player=player).order_by("training__training_date")
    total_goals = appearances.aggregate(total=Sum("goals"))["total"] or 0
    total_assists = appearances.aggregate(total=Sum("assists"))["total"] or 0
    total_apps = appearances.count()
    total_sessions = Training.objects.count()
    sessions_attended = attendance.filter(is_present=True).count()
    if total_sessions > 0:
        attendance_pct = round((sessions_attended / total_sessions) * 100)
    else:
        attendance_pct = 0
    return render(request, "player_performance.html", {
        "player": player,
        "appearances": appearances,
        "attendance": attendance,
        "total_goals": total_goals,
        "total_assists": total_assists,
        "total_apps": total_apps,
        "attendance_pct": attendance_pct,
    })


# Lets players update their own email while keeping club data read only
@login_required
@player_required
def player_profile(request):
    player = Player.objects.get(user=request.user)

    if request.method == "POST":
        form = PlayerProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("PlayerProfile")
    else:
        form = PlayerProfileForm(instance=request.user)

    return render(request, "player_profile.html", {"player": player, "form": form})
