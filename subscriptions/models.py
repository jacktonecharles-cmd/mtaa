from django.db import models

from businesses.models import Business


class Plan(models.Model):
    """
    A subscription plan (Free, Premium, Featured). Database-driven so
    prices/features can change from the admin without a code deploy.
    """

    class PlanCode(models.TextChoices):
        FREE = "free", "Free"
        PREMIUM = "premium", "Premium"
        FEATURED = "featured", "Featured"

    code = models.CharField(max_length=20, choices=PlanCode.choices, unique=True)
    name = models.CharField(max_length=100)
    price_ksh_per_month = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    features = models.TextField(
        blank=True,
        help_text="One feature per line, shown as a bullet list on the pricing page.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["price_ksh_per_month"]

    def __str__(self):
        return f"{self.name} (KSh {self.price_ksh_per_month}/month)"

    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]


class Subscription(models.Model):
    """
    Tracks which plan a business is currently on, and its payment status.

    IMPORTANT: This is intentionally a manual/mock payment status system
    for development. It does NOT process real payments. Marking a
    subscription "active" here is an administrative action (e.g. after
    verifying an M-Pesa payment by hand) until a real payment gateway
    is integrated -- at which point only the code that flips
    `payment_status` needs to change, not this model.
    """

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending Payment"
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"

    business = models.OneToOneField(
        Business, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions")
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    # Manual reference the owner types in (e.g. an M-Pesa transaction code)
    # so an admin can verify and activate the subscription by hand.
    payment_reference = models.CharField(max_length=100, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business.name} - {self.plan.name} ({self.payment_status})"

    @property
    def is_active(self):
        return self.payment_status == self.PaymentStatus.ACTIVE
