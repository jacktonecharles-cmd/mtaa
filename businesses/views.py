from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import BusinessRegistrationForm
from .models import Business, BusinessAnalytics
from categories.models import Category
from locations.models import County, Town, Area
from advertisements.models import Advertisement


@login_required
def business_register(request):
    if request.method == "POST":
        form = BusinessRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()
            BusinessAnalytics.objects.create(business=business)

            if request.user.user_type != request.user.UserType.BUSINESS_OWNER:
                request.user.user_type = request.user.UserType.BUSINESS_OWNER
                request.user.save(update_fields=["user_type"])

            messages.success(
                request,
                f'"{business.name}" was submitted and is pending approval. '
                "We'll notify you once it's live.",
            )
            return redirect("dashboard:overview")
    else:
        form = BusinessRegistrationForm()

    return render(request, "businesses/register.html", {"form": form})


def business_list(request):
    """Search & browse page (Explore)."""
    businesses = Business.objects.filter(
        approval_status=Business.ApprovalStatus.APPROVED
    ).select_related("category", "town", "area")

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "")
    town_slug = request.GET.get("location", "")
    sort = request.GET.get("sort", "relevant")
    premium_only = request.GET.get("premium") == "1"

    if query:
        businesses = businesses.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(services__name__icontains=query)
        ).distinct()

    if category_slug:
        businesses = businesses.filter(category__slug=category_slug)

    if town_slug:
        businesses = businesses.filter(
            Q(town__slug=town_slug) | Q(area__slug=town_slug)
        )

    if premium_only:
        businesses = businesses.filter(is_premium=True)

    businesses = businesses.annotate(
        avg_rating=Avg("reviews__rating"), rating_count=Count("reviews")
    )

    if sort == "rating":
        businesses = businesses.order_by("-avg_rating", "-rating_count")
    elif sort == "newest":
        businesses = businesses.order_by("-created_at")
    elif sort == "featured":
        businesses = businesses.order_by("-is_featured", "-is_premium")
    else:  # "relevant" default -> featured/premium first, then newest
        businesses = businesses.order_by("-is_featured", "-is_premium", "-created_at")

    paginator = Paginator(businesses, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "categories": Category.objects.filter(is_active=True),
        "areas": Area.objects.select_related("town"),
        "query": query,
        "selected_category": category_slug,
        "selected_location": town_slug,
        "sort": sort,
        "premium_only": premium_only,
        "result_count": paginator.count,
    }
    return render(request, "businesses/list.html", context)


def business_detail(request, town_slug, business_slug):
    business = get_object_or_404(
        Business.objects.select_related("category", "town", "county", "area", "owner"),
        slug=business_slug, town__slug=town_slug,
    )

    # Only the approved listing is publicly visible, unless the owner
    # (or an admin) is viewing their own pending/rejected listing.
    is_owner = request.user.is_authenticated and business.owner_id == request.user.id
    if not business.is_approved and not is_owner and not request.user.is_staff:
        from django.http import Http404
        raise Http404("This business is not available.")

    BusinessAnalytics.objects.get_or_create(business=business)
    BusinessAnalytics.objects.filter(business=business).update(
        profile_views=business.analytics.profile_views + 1
    )

    reviews = business.reviews.filter(is_hidden=False).select_related("user").order_by("-created_at")
    similar_businesses = (
        Business.objects.filter(
            category=business.category, approval_status=Business.ApprovalStatus.APPROVED
        )
        .exclude(pk=business.pk)[:4]
    )
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    active_ads = Advertisement.objects.filter(
        business=business, placement=Advertisement.Placement.BUSINESS_PAGE,
        is_active=True, is_approved=True,
        start_date__lte=timezone.localdate(), end_date__gte=timezone.localdate(),
    )

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = business.favorited_by.filter(user=request.user).exists()

    context = {
        "business": business,
        "reviews": reviews,
        "similar_businesses": similar_businesses,
        "user_review": user_review,
        "active_ads": active_ads,
        "is_favorited": is_favorited,
        "is_owner": is_owner,
    }
    return render(request, "businesses/detail.html", context)


@require_POST
def track_click(request, business_id, kind):
    """Lightweight endpoint hit via JS beacon when a visitor clicks
    Call / WhatsApp / Website, so owners can see engagement stats."""
    if kind not in ("phone", "whatsapp", "website"):
        return JsonResponse({"ok": False}, status=400)

    analytics, _ = BusinessAnalytics.objects.get_or_create(business_id=business_id)
    field = {"phone": "phone_clicks", "whatsapp": "whatsapp_clicks", "website": "website_clicks"}[kind]
    setattr(analytics, field, getattr(analytics, field) + 1)
    analytics.save(update_fields=[field, "updated_at"])
    return JsonResponse({"ok": True})
