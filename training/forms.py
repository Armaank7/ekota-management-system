from django import forms
from .models import Training, TrainingAttendance

# Main form used to create or update training sessions
class TrainingForm(forms.ModelForm):
    training_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Training
        fields = ["training_date", "duration", "training_type", "notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["training_type"].choices = [("", "Select training type")] + list(Training.TRAINING_TYPE_CHOICES)


# Form used inside the formset for attendance records
class TrainingAttendanceForm(forms.ModelForm):
    class Meta:
        model = TrainingAttendance
        exclude = ["training"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Unticked means absent, so the extra blank row starts empty
        if not self.instance.pk:
            self.fields["is_present"].initial = False
