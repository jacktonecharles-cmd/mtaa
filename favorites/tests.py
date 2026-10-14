from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from categories.models import Category
from locations.models import County, Town
from businesses.models import Business

from .models import Favorite


class FavoriteTests(TestCase):
    def setUp(self):
        category = Category.objects.get_or_create(name="Barbers")[0]
        county = County.objects.get_or_create(name="Kisumu County")[0]
        town = Town.objects.get_or_create(county=county, name="Kisumu")[0]
        owner = User.objects.create_user(username="owner1", password="pass12345")
        self.user = User.objects.create_user(username="fan1", password="pass12345")
        self.business = Business.objects.create(
            owner=owner, name="Best Cuts", category=category, county=county, town=town,
            approval_status=Business.ApprovalStatus.APPROVED,
        )

    def test_requires_login(self):
        response = self.client.post(reverse("favorites:toggle", args=[self.business.id]))
        self.assertEqual(response.status_code, 302)

    def test_toggle_adds_then_removes_favorite(self):
        self.client.login(username="fan1", password="pass12345")
        self.client.post(reverse("favorites:toggle", args=[self.business.id]))
        self.assertTrue(Favorite.objects.filter(user=self.user, business=self.business).exists())

        self.client.post(reverse("favorites:toggle", args=[self.business.id]))
        self.assertFalse(Favorite.objects.filter(user=self.user, business=self.business).exists())
