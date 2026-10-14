from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("business", "user", "rating", "is_hidden", "created_at")
    list_filter = ("rating", "is_hidden")
    search_fields = ("business__name", "user__username", "comment")
    readonly_fields = ("created_at", "updated_at")
    actions = ["hide_reviews", "unhide_reviews"]

    @admin.action(description="Hide selected reviews (moderation)")
    def hide_reviews(self, request, queryset):
        queryset.update(is_hidden=True)

    @admin.action(description="Unhide selected reviews")
    def unhide_reviews(self, request, queryset):
        queryset.update(is_hidden=False)
