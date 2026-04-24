from django.urls import path
from . import views

# URL patterns for training pages and attendance records
urlpatterns = [
    path("training/", views.staff_training_hub, name="StaffTrainingHub"),
    path("training/<int:training_id>/update/", views.update_training, name="UpdateTraining"),
    path("training/<int:training_id>/delete/", views.delete_training, name="DeleteTraining"),
    path("training/<int:training_id>/attendance/", views.training_attendance, name="TrainingAttendance"),
]
