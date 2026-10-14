from django.contrib import admin

from .models import Business, Service, BusinessPhoto, BusinessAnalytics


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1


class BusinessPhotoInline(admin.TabularInline):
    model = BusinessPhoto
    extra = 1


class BusinessAnalyticsInline(admin.StackedInline):
    model = BusinessAnalytics
    extra = 0
    readonly_fields = (
        "profile_views", "phone_clicks", "whatsapp_clicks", "website_clicks",
    )
    can_delete = False


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "town", "approval_status",
        "is_verified", "is_premium", "is_featured", "created_at",
    )
    list_filter = (
        "approval_status", "is_verified", "is_premium", "is_featured",
        "category", "county", "town",
    )
    search_fields = ("name", "description", "phone_number", "email")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("owner", "category", "county", "town", "area")
    inlines = [ServiceInline, BusinessPhotoInline, BusinessAnalyticsInline]
    actions = ["approve_businesses", "reject_businesses", "mark_featured", "unmark_featured"]

    @admin.action(description="Approve selected businesses")
    def approve_businesses(self, request, queryset):
        updated = queryset.update(approval_status=Business.ApprovalStatus.APPROVED)
        self.message_user(request, f"{updated} business(es) approved.")

    @admin.action(description="Reject selected businesses")
    def reject_businesses(self, request, queryset):
        updated = queryset.update(approval_status=Business.ApprovalStatus.REJECTED)
        self.message_user(request, f"{updated} business(es) rejected.")

    @admin.action(description="Mark selected businesses as featured")
    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Remove featured status from selected businesses")
    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "price")
    search_fields = ("name", "business__name")
    list_filter = ("business__category",)


@admin.register(BusinessPhoto)
class BusinessPhotoAdmin(admin.ModelAdmin):
    list_display = ("business", "caption", "uploaded_at")
    search_fields = ("business__name", "caption")
