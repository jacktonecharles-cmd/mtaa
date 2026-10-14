from django.contrib import admin

from .models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        "title", "business", "placement", "is_approved", "is_active",
        "start_date", "end_date",
    )
    list_filter = ("placement", "is_approved", "is_active")
    search_fields = ("title", "business__name")
    actions = ["approve_ads", "reject_ads"]

    @admin.action(description="Approve selected advertisements")
    def approve_ads(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Reject (unapprove) selected advertisements")
    def reject_ads(self, request, queryset):
        queryset.update(is_approved=False)
