from django.db.models import Avg, Count
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from categories.models import Category
from locations.models import Area
from businesses.models import Business


def home(request):
    """
    Homepage: hero search, popular categories, featured businesses,
    popular (highest-rated) businesses, and browse-by-location.

    Every queryset here degrades gracefully to an empty list when no
    data has been added yet -- the templates show a friendly empty
    state rather than breaking.
    """
    categories = Category.objects.filter(is_active=True)
    areas = Area.objects.select_related("town").all()[:12]

    approved_businesses = Business.objects.filter(
        approval_status=Business.ApprovalStatus.APPROVED
    ).select_related("category", "town")

    featured_businesses = approved_businesses.filter(is_featured=True)[:4]
    popular_businesses = (
        approved_businesses
        .annotate(avg_rating=Avg("reviews__rating"), rating_count=Count("reviews"))
        .order_by("-avg_rating", "-rating_count")[:4]
    )

    context = {
        "categories": categories,
        "areas": areas,
        "featured_businesses": featured_businesses,
        "popular_businesses": popular_businesses,
    }
    return render(request, "home.html", context)


def about(request):
    return render(request, "core/about.html")


def robots_txt(request):
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    content = loader.render_to_string("robots.txt", {"sitemap_url": sitemap_url})
    return HttpResponse(content, content_type="text/plain")
