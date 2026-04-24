from django.urls import path
from . import views

# URL patterns for match pages and appearance records
urlpatterns = [
    path("matches/", views.staff_matches_hub, name="StaffMatchesHub"),
    path("matches/<int:match_id>/update/", views.update_match, name="UpdateMatch"),
    path("matches/<int:match_id>/delete/", views.delete_match, name="DeleteMatch"),
    path("matches/<int:match_id>/appearances/", views.match_appearances, name="MatchAppearances"),
]
