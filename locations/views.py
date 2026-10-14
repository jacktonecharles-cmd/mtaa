from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import render, get_object_or_404

from .models import County, Town, Area
from businesses.models import Business


def location_list(request):
    counties = County.objects.prefetch_related("towns")
    return render(request, "locations/list.html", {"counties": counties})


def location_detail(request, slug):
    """
    A single 'location' page. Matches against Town or Area slugs so
    /location/<slug>/ works for both towns and neighbourhoods.
    """
    town = Town.objects.filter(slug=slug).select_related("county").first()
    area = None if town else Area.objects.filter(slug=slug).select_related("town").first()

    if town:
        businesses = Business.objects.filter(
            town=town, approval_status=Business.ApprovalStatus.APPROVED
        )
        location_name = town.name
        sub_areas = town.areas.all()
    elif area:
        businesses = Business.objects.filter(
            area=area, approval_status=Business.ApprovalStatus.APPROVED
        )
        location_name = f"{area.name}, {area.town.name}"
        sub_areas = []
        town = area.town
    else:
        from django.http import Http404
        raise Http404("Location not found.")

    businesses = (
        businesses.select_related("category", "town")
        .annotate(avg_rating=Avg("reviews__rating"), rating_count=Count("reviews"))
        .order_by("-is_featured", "-is_premium", "-created_at")
    )
    paginator = Paginator(businesses, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request, "locations/detail.html",
        {
            "location_name": location_name, "town": town, "area": area,
            "sub_areas": sub_areas, "page_obj": page_obj, "result_count": paginator.count,
        },
    )
