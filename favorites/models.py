from django.conf import settings
from django.db import models

from businesses.models import Business


class Favorite(models.Model):
    """A saved/favorited business for a logged-in user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites"
    )
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "business"], name="one_favorite_per_user_per_business"
            )
        ]

    def __str__(self):
        return f"{self.user} \u2764 {self.business.name}"
