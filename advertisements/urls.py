from django.urls import path

from . import views

app_name = "advertisements"

urlpatterns = [
    path("request/<int:business_id>/", views.request_ad, name="request"),
]
