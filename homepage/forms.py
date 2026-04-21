from django import forms
from django.contrib.auth.models import User


# Form used by staff to update their own account details
class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


# Form used by players to update their own email address
class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
