from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("pricing/", views.pricing, name="pricing"),
    path("upgrade/<int:business_id>/<str:plan_code>/", views.request_upgrade, name="request_upgrade"),
]
