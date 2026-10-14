from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Favorite
from businesses.models import Business


@login_required
@require_POST
def toggle_favorite(request, business_id):
    business = get_object_or_404(Business, pk=business_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, business=business)

    if not created:
        favorite.delete()
        messages.info(request, f"Removed {business.name} from your favorites.")
    else:
        messages.success(request, f"Saved {business.name} to your favorites.")

    next_url = request.POST.get("next") or business.get_absolute_url()
    return redirect(next_url)


@login_required
def my_favorites(request):
    favorites = (
        Favorite.objects.filter(user=request.user)
        .select_related("business", "business__category", "business__town")
    )
    return render(request, "favorites/list.html", {"favorites": favorites})
