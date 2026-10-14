from django.urls import path

from . import views

app_name = "businesses"

urlpatterns = [
    path("register/", views.business_register, name="register"),
    path("explore/", views.business_list, name="list"),
    path("track/<int:business_id>/<str:kind>/", views.track_click, name="track_click"),
    path("<slug:town_slug>/<slug:business_slug>/", views.business_detail, name="business_detail"),
]
