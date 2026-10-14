from django.db import models
from django.utils.text import slugify


class County(models.Model):
    """
    A Kenyan county, e.g. Kisumu County.
    Seeded initially with Kisumu; more counties can be added later
    (there are 47 in total) without any model changes.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Counties"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Town(models.Model):
    """
    A town/city within a county, e.g. Kisumu City within Kisumu County.
    """
    county = models.ForeignKey(
        County, on_delete=models.CASCADE, related_name="towns"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("county", "name")
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.name}, {self.county.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.county.name}")
        super().save(*args, **kwargs)


class Area(models.Model):
    """
    A neighbourhood/estate within a town, e.g. Kondele within Kisumu.
    """
    town = models.ForeignKey(
        Town, on_delete=models.CASCADE, related_name="areas"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("town", "name")
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.name}, {self.town.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.town.name}")
        super().save(*args, **kwargs)
