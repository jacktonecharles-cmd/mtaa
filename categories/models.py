from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    A business category, e.g. Salons, Barbers, Restaurants.
    Fully database-driven: admins can add/edit/delete categories
    from the Django admin without touching code.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome icon class, e.g. 'fa-solid fa-scissors'",
    )
    description = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers appear first."
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
