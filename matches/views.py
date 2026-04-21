from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from accounts.decorators import staff_required
from .models import Match, MatchAppearance
from .forms import MatchForm, MatchAppearanceForm

# @login_required makes sure that you can only access this confidential page if you are signed in - prevents unauthorised access
@login_required
@staff_required
def staff_matches_hub(request):
    form = MatchForm()

    if request.method == "POST":

        # CREATE MATCH
        if "opponent_name" in request.POST:
            form = MatchForm(request.POST)
            if form.is_valid():
                match = form.save(commit=False)
                # Home matches are always at Mayfield
                if match.venue_type == "Home":
                    match.location = "Mayfield"
                match.save()
                messages.success(request, "Match added successfully!")
                return redirect("StaffMatchesHub")

        # DELETE MATCH
        elif "deleteMatchID" in request.POST:
            match_id = request.POST.get("deleteMatchID")
            match = Match.objects.get(id=match_id)
            match.delete()
            messages.success(request, "Match deleted")
            return redirect("StaffMatchesHub")

    # Order by match date
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    matches = Match.objects.filter(
        Q(opponent_name__icontains=q) | Q(match_type__icontains=q) | Q(venue_type__icontains=q)
    ).order_by("match_date")
    return render(request, "staff_matches_hub.html", {
        "matches": matches,
        "form": form,
        "q": q
    })


 # UPDATE MATCH
@login_required
@staff_required
def update_match(request, match_id):

    match = Match.objects.get(id=match_id)

    if request.method == "POST":
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            updated = form.save(commit=False)
            # Home matches are always at Mayfield
            if updated.venue_type == "Home":
                updated.location = "Mayfield"
            updated.save()
            messages.success(request, "Match updated successfully!")
            return redirect("StaffMatchesHub")
    else:
        form = MatchForm(instance=match)

    return render(request, "update_match.html", {"match": match, "form": form})


# Adds, updates and deletes player appearance records for one match
@login_required
@staff_required
def match_appearances(request, match_id):

    match = Match.objects.get(id=match_id)
    AppearanceFormSet = modelformset_factory(MatchAppearance, form=MatchAppearanceForm, extra=1, can_delete=True)

    if request.method == "POST":
        formset = AppearanceFormSet(request.POST, queryset=MatchAppearance.objects.filter(match=match))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.match = match
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, "Appearances saved")
            return redirect("MatchAppearances", match_id=match.id)
    else:
        formset = AppearanceFormSet(queryset=MatchAppearance.objects.filter(match=match))

    return render(request, "match_appearances.html", {"match": match, "formset": formset})
