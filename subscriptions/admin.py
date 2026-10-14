from django.contrib import admin

from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "price_ksh_per_month", "is_active")
    list_filter = ("is_active",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "business", "plan", "payment_status", "started_at", "expires_at",
    )
    list_filter = ("payment_status", "plan")
    search_fields = ("business__name", "payment_reference")
    readonly_fields = ("created_at", "updated_at")
    actions = ["activate_subscriptions", "expire_subscriptions"]

    @admin.action(description="Activate selected subscriptions (after verifying payment)")
    def activate_subscriptions(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()
        for sub in queryset:
            sub.payment_status = Subscription.PaymentStatus.ACTIVE
            sub.started_at = now
            sub.expires_at = now + timedelta(days=30)
            sub.save()
            sub.business.is_premium = sub.plan.code in ("premium", "featured")
            sub.business.is_featured = sub.plan.code == "featured"
            sub.business.save()
        self.message_user(request, f"{queryset.count()} subscription(s) activated.")

    @admin.action(description="Mark selected subscriptions as expired")
    def expire_subscriptions(self, request, queryset):
        for sub in queryset:
            sub.payment_status = Subscription.PaymentStatus.EXPIRED
            sub.save()
            sub.business.is_premium = False
            sub.business.is_featured = False
            sub.business.save()
