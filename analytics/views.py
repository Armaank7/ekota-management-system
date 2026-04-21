from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, Avg
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from accounts.models import Player
from accounts.decorators import staff_required, player_required
from matches.models import Match, MatchAppearance
from training.models import Training, TrainingAttendance


# Helper function so tied players are not cut off from the top 5 lists
def get_top5_with_ties(rows, key):
    # Include all players tied at 5th place, not just the first 5
    if len(rows) <= 5:
        return rows
    threshold = rows[4][key]
    return [row for row in rows if row[key] >= threshold]


def add_ranks(rows, key):
    # Gives players the same rank if they are tied on the same stat
    current_rank = 0
    previous_value = None

    for row in rows:
        if row[key] != previous_value:
            current_rank += 1
            previous_value = row[key]
        row["rank"] = current_rank

    return rows


# Main analytics dashboard for staff
@login_required
@staff_required
def staff_analytics(request):
    # Match record
    matches = Match.objects.all()
    wins = matches.filter(our_score__gt=F("opponent_score")).count()
    draws = matches.filter(our_score=F("opponent_score")).count()
    losses = matches.filter(our_score__lt=F("opponent_score")).count()
    total_scored = matches.aggregate(total=Sum("our_score"))["total"] or 0
    total_conceded = matches.aggregate(total=Sum("opponent_score"))["total"] or 0

    # Top scorers
    all_scorers = list(
        MatchAppearance.objects.values("player__first_name", "player__last_name")
        .annotate(total_goals=Sum("goals"))
        .order_by("-total_goals")
    )
    top_scorers = add_ranks(get_top5_with_ties(all_scorers, "total_goals"), "total_goals")

    # Top assisters
    all_assisters = list(
        MatchAppearance.objects.values("player__first_name", "player__last_name")
        .annotate(total_assists=Sum("assists"))
        .order_by("-total_assists")
    )
    top_assisters = add_ranks(get_top5_with_ties(all_assisters, "total_assists"), "total_assists")

    # Most appearances (top 5)
    most_appearances = add_ranks(list(
        MatchAppearance.objects.values("player__first_name", "player__last_name")
        .annotate(total_apps=Count("id"))
        .order_by("-total_apps")[:5]
    ), "total_apps")

    # Players by position for pie chart
    total_players = Player.objects.count()
    position_counts = list(Player.objects.values("position").annotate(count=Count("id")))

    # Average goals scored per match by month
    monthly_goals = (
        matches.annotate(month=TruncMonth("match_date"))
        .values("month")
        .annotate(avg_goals=Avg("our_score"))
        .order_by("month")
    )

    # Average goals conceded per match by month
    monthly_goals_conceded = (
        matches.annotate(month=TruncMonth("match_date"))
        .values("month")
        .annotate(avg_goals_conceded=Avg("opponent_score"))
        .order_by("month")
    )

    # Training attendance % per player for bar chart
    total_sessions = Training.objects.count()
    attendance_rates = []
    if total_sessions > 0:
        rates = (
            TrainingAttendance.objects.filter(is_present=True)
            .values("player__first_name", "player__last_name")
            .annotate(sessions_attended=Count("id"))
            .order_by("player__last_name")
        )
        for rate in rates:
            pct = round((rate["sessions_attended"] / total_sessions) * 100)
            attendance_rates.append({
                "name": f"{rate['player__first_name']} {rate['player__last_name']}",
                "pct": pct,
            })

    return render(request, "staff_analytics.html", {
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "total_played": wins + draws + losses,
        "total_scored": total_scored,
        "total_conceded": total_conceded,
        "top_scorers": top_scorers,
        "top_assisters": top_assisters,
        "most_appearances": most_appearances,
        "total_players": total_players,
        "position_counts": position_counts,
        "monthly_goals": monthly_goals,
        "monthly_goals_conceded": monthly_goals_conceded,
        "attendance_rates": attendance_rates,
    })


# Shows full stats for one player on the staff side
@login_required
@staff_required
def player_stats(request, player_id):
    player = Player.objects.get(id=player_id)
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

    return render(request, "player_stats.html", {
        "player": player,
        "appearances": appearances,
        "attendance": attendance,
        "total_goals": total_goals,
        "total_assists": total_assists,
        "total_apps": total_apps,
        "attendance_pct": attendance_pct,
    })
