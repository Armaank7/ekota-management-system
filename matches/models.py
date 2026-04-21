from django.db import models

# Stores the main fixture and result details for each match
class Match(models.Model):
    # List of match categories shown in the form dropdown
    MATCH_TYPE_CHOICES = [
        ("League", "League"),
        ("Cup", "Cup"),
        ("Friendly", "Friendly"),
    ]

    # List of venue types shown in the form dropdown
    VENUE_TYPE_CHOICES = [
        ("Home", "Home"),
        ("Away", "Away"),
        ("Neutral", "Neutral"),
    ]

    opponent_name = models.CharField(max_length=100)
    match_date = models.DateField()
    match_type = models.CharField(max_length=10, choices=MATCH_TYPE_CHOICES)
    venue_type = models.CharField(max_length=10, choices=VENUE_TYPE_CHOICES)
    location = models.CharField(max_length=150)
    our_score = models.IntegerField()
    opponent_score = models.IntegerField()

    def __str__(self):
        return f"{self.opponent_name} ({self.match_date})"


# Stores each player's appearance record for a match
class MatchAppearance(models.Model):
    player = models.ForeignKey("accounts.Player", on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)

    # Stops the same player being added twice to one match
    class Meta:
        unique_together = ("player", "match")

    def __str__(self):
        return f"{self.player} in {self.match}"
