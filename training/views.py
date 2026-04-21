from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from accounts.decorators import staff_required
from .models import Training, TrainingAttendance
from .forms import TrainingForm, TrainingAttendanceForm

# @login_required makes sure that you can only access this confidential page if you are signed in - prevents unauthorised access
@login_required
@staff_required
def staff_training_hub(request):
    form = TrainingForm()

    if request.method == "POST":

        # CREATE TRAINING SESSION
        if "training_date" in request.POST:
            form = TrainingForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Training session added successfully!")
                return redirect("StaffTrainingHub")

        # DELETE TRAINING SESSION
        elif "deleteTrainingID" in request.POST:
            training_id = request.POST.get("deleteTrainingID")
            training = Training.objects.get(id=training_id)
            training.delete()
            messages.success(request, "Training session deleted")
            return redirect("StaffTrainingHub")

    # Order by training date
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    sessions = Training.objects.filter(
        Q(training_type__icontains=q) | Q(notes__icontains=q)
    ).order_by("training_date")
    return render(request, "staff_training_hub.html", {
        "sessions": sessions,
        "form": form,
        "q": q
    })


 # UPDATE TRAINING SESSION
@login_required
@staff_required
def update_training(request, training_id):

    training = Training.objects.get(id=training_id)

    if request.method == "POST":
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            messages.success(request, "Training session updated successfully!")
            return redirect("StaffTrainingHub")
    else:
        form = TrainingForm(instance=training)

    return render(request, "update_training.html", {"training": training, "form": form})


# Adds, updates and deletes attendance records for one training session
@login_required
@staff_required
def training_attendance(request, training_id):

    training = Training.objects.get(id=training_id)
    AttendanceFormSet = modelformset_factory(TrainingAttendance, form=TrainingAttendanceForm, extra=1, can_delete=True)

    if request.method == "POST":
        formset = AttendanceFormSet(request.POST, queryset=TrainingAttendance.objects.filter(training=training))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.training = training
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, "Attendance saved")
            return redirect("TrainingAttendance", training_id=training.id)
    else:
        formset = AttendanceFormSet(queryset=TrainingAttendance.objects.filter(training=training))

    return render(request, "training_attendance.html", {"training": training, "formset": formset})
