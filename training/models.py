from django.db import models

# Stores the main details for each training session
class Training(models.Model):
    # List of training categories shown in the form dropdown
    TRAINING_TYPE_CHOICES = [
        ("Attacking", "Attacking"),
        ("Defending", "Defending"),
        ("Passing", "Passing"),
        ("Fitness", "Fitness"),
        ("Match Sim", "Match Sim"),
    ]

    training_date = models.DateField()
    duration = models.IntegerField()
    training_type = models.CharField(max_length=15, choices=TRAINING_TYPE_CHOICES)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.training_type} ({self.training_date})"


# Stores each player's attendance record for a training session
class TrainingAttendance(models.Model):
    player = models.ForeignKey("accounts.Player", on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)

    is_present = models.BooleanField(default=True)
    player_notes = models.TextField(blank=True)

    # Stops the same player being added twice to one training session
    class Meta:
        unique_together = ("player", "training")

    def __str__(self):
        return f"{self.player} - {self.training}"
