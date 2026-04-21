from django.db import models
from django.contrib.auth.models import User

# Stores the staff account linked to the built in Django user
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staffID = models.CharField(max_length=20, unique=True, blank=True, default="")

    def __str__(self):
        return f"Staff: {self.user.username}"

# Stores the main player details used across the app
class Player(models.Model):
    POSITION_CHOICES = [   # List of possible position categories - represented as dropdown menu
        ("GK", "GK"),
        ("DEF", "DEF"),
        ("MID", "MID"),
        ("FWD", "FWD"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    # These details are managed by staff when creating and updating a player
    playerID = models.CharField(max_length=20, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    date_of_birth = models.DateField()
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    must_change_password = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
