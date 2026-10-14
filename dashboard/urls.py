from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("business/edit/", views.edit_business, name="edit_business"),
    path("services/", views.services, name="services"),
    path("services/<int:service_id>/delete/", views.service_delete, name="service_delete"),
    path("photos/", views.photos, name="photos"),
    path("photos/<int:photo_id>/delete/", views.photo_delete, name="photo_delete"),
    path("reviews/", views.reviews_view, name="reviews"),
    path("subscription/", views.subscription_view, name="subscription"),
    path("advertise/", views.advertise_view, name="advertise"),
]
