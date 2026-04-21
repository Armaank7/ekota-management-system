from django.urls import path
from . import views

# URL patterns for the landing page and both dashboards
urlpatterns = [
    path("", views.landing_page, name="LandingPage"),
    path("staff/homepage/", views.staff_homepage, name="StaffHomepage"),
    path("player/homepage/", views.player_homepage, name="PlayerHomepage"),
    path("player/fixtures/", views.player_match_fixtures, name="PlayerFixtures"),
    path("player/training/", views.player_training_sessions, name="PlayerTraining"),
    path("player/performance/", views.player_performance, name="PlayerPerformance"),
    path("player/profile/", views.player_profile, name="PlayerProfile"),
    path("staff/profile/", views.staff_profile, name="StaffProfile"),
]
