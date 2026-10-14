from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AdvertisementRequestForm
from businesses.models import Business


@login_required
def request_ad(request, business_id):
    business = get_object_or_404(Business, pk=business_id, owner=request.user)

    if request.method == "POST":
        form = AdvertisementRequestForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.business = business
            ad.is_approved = False
            ad.save()
            messages.success(
                request,
                "Advertisement submitted for review. An admin will approve it before it goes live.",
            )
            return redirect("dashboard:advertise")
    else:
        form = AdvertisementRequestForm()

    return render(request, "advertisements/request_ad.html", {"form": form, "business": business})
