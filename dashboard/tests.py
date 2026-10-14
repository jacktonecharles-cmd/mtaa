from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from categories.models import Category
from locations.models import County, Town
from businesses.models import Business


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.category = Category.objects.get_or_create(name="Barbers")[0]
        self.county = County.objects.get_or_create(name="Kisumu County")[0]
        self.town = Town.objects.get_or_create(county=self.county, name="Kisumu")[0]
        self.owner = User.objects.create_user(username="owner1", password="pass12345")
        self.other_user = User.objects.create_user(username="stranger", password="pass12345")
        self.business = Business.objects.create(
            owner=self.owner, name="Best Cuts", category=self.category,
            county=self.county, town=self.town,
            approval_status=Business.ApprovalStatus.APPROVED,
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard:overview"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_owner_sees_their_business_in_dashboard(self):
        self.client.login(username="owner1", password="pass12345")
        response = self.client.get(reverse("dashboard:overview"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Best Cuts")

    def test_user_with_no_business_redirected_to_register(self):
        self.client.login(username="stranger", password="pass12345")
        response = self.client.get(reverse("dashboard:overview"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("businesses:register"), response.url)
