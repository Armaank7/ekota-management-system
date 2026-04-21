from django import forms
from accounts.models import Player

# Main form used to add or update a player profile
class PlayerForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Player
        fields = ["first_name", "last_name", "date_of_birth", "position"]

# Separate form used to create the player's login details
class PlayerUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
