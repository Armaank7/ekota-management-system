from django.urls import path
from . import views

# URL patterns for the analytics dashboard and player stats page
urlpatterns = [
    path("analytics/", views.staff_analytics, name="StaffAnalytics"),
    path("analytics/player/<int:player_id>/", views.player_stats, name="PlayerStats"),
]
