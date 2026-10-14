from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from businesses.forms import BusinessEditForm, ServiceForm, BusinessPhotoForm
from businesses.models import Business, Service, BusinessPhoto, BusinessAnalytics
from reviews.models import Review
from reviews.forms import OwnerResponseForm
from subscriptions.models import Plan, Subscription
from advertisements.models import Advertisement


def _get_owner_business(request):
    """
    MVP simplification: a business owner manages one business from the
    dashboard (the first one they registered). Multi-business management
    per owner is a natural later extension of this same view.
    """
    return Business.objects.filter(owner=request.user).select_related(
        "category", "county", "town", "area"
    ).first()


@login_required
def overview(request):
    business = _get_owner_business(request)
    if not business:
        messages.info(request, "You don't have a business yet — register one to see your dashboard.")
        return redirect("businesses:register")

    analytics, _ = BusinessAnalytics.objects.get_or_create(business=business)
    review_count = business.review_count
    average_rating = business.average_rating

    context = {
        "business": business,
        "analytics": analytics,
        "review_count": review_count,
        "average_rating": average_rating,
    }
    return render(request, "dashboard/overview.html", context)


@login_required
def edit_business(request):
    business = _get_owner_business(request)
    if not business:
        return redirect("businesses:register")

    if request.method == "POST":
        form = BusinessEditForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, "Business details updated.")
            return redirect("dashboard:overview")
    else:
        form = BusinessEditForm(instance=business)

    return render(request, "dashboard/edit_business.html", {"form": form, "business": business})


@login_required
def services(request):
    business = _get_owner_business(request)
    if not business:
        return redirect("businesses:register")

    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.business = business
            service.save()
            messages.success(request, f'Added service "{service.name}".')
            return redirect("dashboard:services")
    else:
        form = ServiceForm()

    return render(
        request, "dashboard/services.html",
        {"business": business, "services": business.services.all(), "form": form},
    )


@login_required
def service_delete(request, service_id):
    business = _get_owner_business(request)
    service = get_object_or_404(Service, pk=service_id, business=business)
    service.delete()
    messages.info(request, "Service removed.")
    return redirect("dashboard:services")


@login_required
def photos(request):
    business = _get_owner_business(request)
    if not business:
        return redirect("businesses:register")

    if request.method == "POST":
        form = BusinessPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.business = business
            photo.save()
            messages.success(request, "Photo uploaded.")
            return redirect("dashboard:photos")
    else:
        form = BusinessPhotoForm()

    return render(
        request, "dashboard/photos.html",
        {"business": business, "photos": business.photos.all(), "form": form},
    )


@login_required
def photo_delete(request, photo_id):
    business = _get_owner_business(request)
    photo = get_object_or_404(BusinessPhoto, pk=photo_id, business=business)
    photo.delete()
    messages.info(request, "Photo removed.")
    return redirect("dashboard:photos")


@login_required
def reviews_view(request):
    business = _get_owner_business(request)
    if not business:
        return redirect("businesses:register")

    reviews = business.reviews.select_related("user").order_by("-created_at")
    response_form = OwnerResponseForm()

    return render(
        request, "dashboard/reviews.html",
        {"business": business, "reviews": reviews, "response_form": response_form},
    )


@login_required
def subscription_view(request):
    business = _get_owner_business(request)
    if not business:
        return redirect("businesses:register")

    subscription = Subscription.objects.filter(business=business).select_related("plan").first()
    plans = Plan.objects.filter(is_active=True)

    return render(
        request, "dashboard/subscription.html",
        {"business": business, "subscription": subscription, "plans": plans},
    )


@login_required
def advertise_view(request):
    business = _get_owner_business(request)
    if not business:
        return redirect("businesses:register")

    ads = Advertisement.objects.filter(business=business).order_by("-created_at")
    return render(request, "dashboard/advertise.html", {"business": business, "ads": ads})
