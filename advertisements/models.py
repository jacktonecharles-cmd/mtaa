from django.db import models

from businesses.models import Business


class Advertisement(models.Model):
    """
    A paid advertisement banner belonging to a business, shown in an
    approved placement for a date range. Admins must approve ads before
    they go live (is_approved), and `is_currently_active` combines that
    with the active flag and date range.
    """

    class Placement(models.TextChoices):
        HOMEPAGE = "homepage", "Homepage"
        SEARCH_RESULTS = "search_results", "Search Results"
        CATEGORY_PAGE = "category_page", "Category Page"
        BUSINESS_PAGE = "business_page", "Business Page"

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="advertisements"
    )
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="advertisements/")
    destination_url = models.URLField()
    placement = models.CharField(max_length=20, choices=Placement.choices)
    price_ksh = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    start_date = models.DateField()
    end_date = models.DateField()

    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True, help_text="Owner/admin can pause an ad without deleting it."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["placement", "is_active", "is_approved"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_placement_display()})"

    @property
    def is_currently_active(self):
        from django.utils import timezone
        today = timezone.localdate()
        return (
            self.is_active
            and self.is_approved
            and self.start_date <= today <= self.end_date
        )
