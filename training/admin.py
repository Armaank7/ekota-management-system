from django.contrib import admin
from .models import Training, TrainingAttendance

# Register training models so they can be managed in admin
admin.site.register(Training)
admin.site.register(TrainingAttendance)
