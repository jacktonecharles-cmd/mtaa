from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from businesses.models import Business


class Review(models.Model):
    """
    A 1-5 star review left by a logged-in user on a business.
    A user may only have one review per business (they edit it instead
    of creating duplicates), enforced at the database level below.
    """

    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)

    # Business owner's public reply to this review.
    owner_response = models.TextField(blank=True)
    owner_response_at = models.DateTimeField(null=True, blank=True)

    is_hidden = models.BooleanField(
        default=False, help_text="Hidden by an administrator during moderation."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["business", "user"], name="one_review_per_user_per_business"
            )
        ]
        indexes = [
            models.Index(fields=["business", "rating"]),
        ]

    def __str__(self):
        return f"{self.rating}\u2605 review of {self.business.name} by {self.user}"
