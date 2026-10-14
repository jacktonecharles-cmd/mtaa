from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from categories.models import Category
from locations.models import County, Town, Area


def business_logo_path(instance, filename):
    return f"businesses/{instance.slug}/logo/{filename}"


def business_cover_path(instance, filename):
    return f"businesses/{instance.slug}/cover/{filename}"


class Business(models.Model):
    """
    A business listing. This is the core model of the platform.
    """

    class ApprovalStatus(models.TextChoices):
        PENDING = "pending", "Pending Approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    # --- Ownership & core info -------------------------------------------------
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="businesses",
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="businesses"
    )

    # --- Location ----------------------------------------------------------
    county = models.ForeignKey(
        County, on_delete=models.PROTECT, related_name="businesses"
    )
    town = models.ForeignKey(
        Town, on_delete=models.PROTECT, related_name="businesses"
    )
    area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="businesses",
    )
    address = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    # --- Content -------------------------------------------------------------
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to=business_logo_path, blank=True, null=True)
    cover_image = models.ImageField(
        upload_to=business_cover_path, blank=True, null=True
    )
    opening_hours = models.TextField(
        blank=True,
        help_text="e.g. Mon-Sat: 8:00 AM - 6:00 PM, Sun: Closed",
    )

    # --- Contact -------------------------------------------------------------
    phone_number = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    # --- Social media --------------------------------------------------------
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    # --- Status flags --------------------------------------------------------
    approval_status = models.CharField(
        max_length=10, choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
    )
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    # --- Timestamps ------------------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Businesses"
        ordering = ["-is_featured", "-is_premium", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["approval_status"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["is_premium"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.town.name if self.town_id else ''}")
            slug = base_slug
            counter = 1
            while Business.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "businesses:business_detail",
            kwargs={"town_slug": self.town.slug, "business_slug": self.slug},
        )

    @property
    def is_approved(self):
        return self.approval_status == self.ApprovalStatus.APPROVED

    @property
    def average_rating(self):
        agg = self.reviews.aggregate(models.Avg("rating"))
        return round(agg["rating__avg"] or 0, 1)

    @property
    def review_count(self):
        return self.reviews.count()


class Service(models.Model):
    """A service/product offered by a business, with an optional price."""

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="services"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Price in KSh. Leave blank if variable/on request.",
    )
    image = models.ImageField(
        upload_to="services/", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.business.name})"


class BusinessPhoto(models.Model):
    """Additional gallery photos for a business."""

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to="business_photos/")
    caption = models.CharField(max_length=150, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"Photo for {self.business.name}"


class BusinessAnalytics(models.Model):
    """
    Simple counters used to show basic statistics on the owner dashboard.
    One row per business, incremented as visitors interact with the page.
    """

    business = models.OneToOneField(
        Business, on_delete=models.CASCADE, related_name="analytics"
    )
    profile_views = models.PositiveIntegerField(default=0)
    phone_clicks = models.PositiveIntegerField(default=0)
    whatsapp_clicks = models.PositiveIntegerField(default=0)
    website_clicks = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Business analytics"

    def __str__(self):
        return f"Analytics for {self.business.name}"
