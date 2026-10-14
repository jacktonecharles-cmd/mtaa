from django.urls import path

from . import views

app_name = "favorites"

urlpatterns = [
    path("", views.my_favorites, name="list"),
    path("toggle/<int:business_id>/", views.toggle_favorite, name="toggle"),
]
