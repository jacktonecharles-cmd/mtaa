from django.contrib.sitemaps import Sitemap

from businesses.models import Business
from categories.models import Category
from locations.models import Town, Area


class BusinessSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Business.objects.filter(approval_status=Business.ApprovalStatus.APPROVED)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.filter(is_active=True)

    def location(self, obj):
        return f"/category/{obj.slug}/"


class LocationSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return list(Town.objects.all()) + list(Area.objects.all())

    def location(self, obj):
        return f"/location/{obj.slug}/"


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ["core:home", "core:about", "businesses:list", "categories:list", "locations:list"]

    def location(self, item):
        from django.urls import reverse
        return reverse(item)
