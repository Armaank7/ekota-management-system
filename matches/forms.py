from django import forms
from .models import Match, MatchAppearance

# Main form used to create or update match records
class MatchForm(forms.ModelForm):
    match_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Match
        fields = ["opponent_name", "match_date", "match_type", "venue_type", "location", "our_score", "opponent_score"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["match_type"].choices = [("", "Select match type")] + list(Match.MATCH_TYPE_CHOICES)
        self.fields["venue_type"].choices = [("", "Select venue")] + list(Match.VENUE_TYPE_CHOICES)


# Form used inside the formset for match appearance records
class MatchAppearanceForm(forms.ModelForm):
    class Meta:
        model = MatchAppearance
        exclude = ["match"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Clears the default values on the extra blank row in the formset
        if not self.instance.pk:
            self.fields["goals"].initial = None
            self.fields["assists"].initial = None
            self.fields["minutes_played"].initial = None
