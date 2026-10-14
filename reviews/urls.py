from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("business/<int:business_id>/add/", views.add_or_update_review, name="add"),
    path("<int:review_id>/respond/", views.owner_respond, name="respond"),
]
