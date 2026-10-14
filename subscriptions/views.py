from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SubscriptionRequestForm
from .models import Plan, Subscription
from businesses.models import Business


def pricing(request):
    plans = Plan.objects.filter(is_active=True)
    return render(request, "subscriptions/pricing.html", {"plans": plans})


@login_required
def request_upgrade(request, business_id, plan_code):
    business = get_object_or_404(Business, pk=business_id, owner=request.user)
    plan = get_object_or_404(Plan, code=plan_code, is_active=True)

    subscription, _ = Subscription.objects.get_or_create(
        business=business, defaults={"plan": plan}
    )

    if request.method == "POST":
        form = SubscriptionRequestForm(request.POST, instance=subscription)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.plan = plan
            subscription.payment_status = Subscription.PaymentStatus.PENDING
            subscription.save()
            messages.success(
                request,
                "Upgrade request received. This is a manual process for now — "
                "an admin will verify payment and activate your plan.",
            )
            return redirect("dashboard:subscription")
    else:
        form = SubscriptionRequestForm(instance=subscription)

    return render(
        request, "subscriptions/request_upgrade.html",
        {"form": form, "plan": plan, "business": business},
    )
