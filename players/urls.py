from django.urls import path
from . import views

# URL patterns for the staff player management pages
urlpatterns = [
    path("staff/players/", views.staff_players_hub, name="StaffPlayersHub"),
    path("staff/players/<int:player_id>/update/", views.update_player, name="UpdatePlayer"),
    path("staff/players/<int:player_id>/delete/", views.delete_player, name="DeletePlayer"),
]
