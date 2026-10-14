from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ReviewForm, OwnerResponseForm
from .models import Review
from businesses.models import Business


@login_required
@require_POST
def add_or_update_review(request, business_id):
    business = get_object_or_404(Business, pk=business_id, approval_status=Business.ApprovalStatus.APPROVED)

    if business.owner_id == request.user.id:
        messages.error(request, "You can't review your own business.")
        return redirect(business.get_absolute_url())

    existing = Review.objects.filter(business=business, user=request.user).first()
    form = ReviewForm(request.POST, instance=existing)

    if form.is_valid():
        review = form.save(commit=False)
        review.business = business
        review.user = request.user
        review.save()
        messages.success(request, "Thanks — your review has been posted.")
    else:
        messages.error(request, "Please choose a rating between 1 and 5.")

    return redirect(business.get_absolute_url())


@require_POST
def owner_respond(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if not request.user.is_authenticated or review.business.owner_id != request.user.id:
        messages.error(request, "You don't have permission to respond to this review.")
        return redirect("core:home")

    form = OwnerResponseForm(request.POST, instance=review)
    if form.is_valid():
        review = form.save(commit=False)
        review.owner_response_at = timezone.now()
        review.save()
        messages.success(request, "Your response has been posted.")

    return redirect(review.business.get_absolute_url())
