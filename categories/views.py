from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import render, get_object_or_404

from .models import Category
from businesses.models import Business


def category_list(request):
    categories = Category.objects.filter(is_active=True).annotate(
        business_count=Count(
            "businesses",
            filter=Q(businesses__approval_status=Business.ApprovalStatus.APPROVED),
        )
    )
    return render(request, "categories/list.html", {"categories": categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    businesses = (
        Business.objects.filter(category=category, approval_status=Business.ApprovalStatus.APPROVED)
        .select_related("town", "area")
        .annotate(avg_rating=Avg("reviews__rating"), rating_count=Count("reviews"))
        .order_by("-is_featured", "-is_premium", "-created_at")
    )
    paginator = Paginator(businesses, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request, "categories/detail.html",
        {"category": category, "page_obj": page_obj, "result_count": paginator.count},
    )
