from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from categories.models import Category
from locations.models import County, Town, Area
from reviews.models import Review

from .models import Business


class BusinessTestBase(TestCase):
    def setUp(self):
        self.category = Category.objects.get_or_create(name="Barbers")[0]
        self.county = County.objects.get_or_create(name="Kisumu County")[0]
        self.town = Town.objects.get_or_create(county=self.county, name="Kisumu")[0]
        self.area = Area.objects.get_or_create(town=self.town, name="CBD")[0]
        self.owner = User.objects.create_user(username="owner1", password="pass12345")


class SlugGenerationTests(BusinessTestBase):
    def test_slug_is_auto_generated_and_unique(self):
        b1 = Business.objects.create(
            owner=self.owner, name="Best Cuts", category=self.category,
            county=self.county, town=self.town,
        )
        self.assertEqual(b1.slug, "best-cuts-kisumu")

        owner2 = User.objects.create_user(username="owner2", password="pass12345")
        b2 = Business.objects.create(
            owner=owner2, name="Best Cuts", category=self.category,
            county=self.county, town=self.town,
        )
        # Same name -> slug must be de-duplicated, not collide.
        self.assertNotEqual(b1.slug, b2.slug)
        self.assertTrue(Business.objects.filter(slug=b2.slug).exists())


class BusinessRegistrationTests(BusinessTestBase):
    def test_registration_requires_login(self):
        response = self.client.get(reverse("businesses:register"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_register_business(self):
        self.client.login(username="owner1", password="pass12345")
        response = self.client.post(reverse("businesses:register"), {
            "name": "Best Cuts Kisumu",
            "category": self.category.id,
            "county": self.county.id,
            "town": self.town.id,
            "area": self.area.id,
            "description": "Top barber shop",
            "phone_number": "0712345678",
            "whatsapp_number": "", "email": "", "website": "",
            "address": "", "opening_hours": "",
            "facebook_url": "", "instagram_url": "", "tiktok_url": "", "twitter_url": "",
        })
        self.assertEqual(response.status_code, 302)
        business = Business.objects.get(name="Best Cuts Kisumu")
        self.assertEqual(business.owner, self.owner)
        # New businesses start pending, not publicly approved.
        self.assertEqual(business.approval_status, Business.ApprovalStatus.PENDING)

        self.owner.refresh_from_db()
        self.assertEqual(self.owner.user_type, self.owner.UserType.BUSINESS_OWNER)


class BusinessApprovalVisibilityTests(BusinessTestBase):
    def test_pending_business_not_publicly_visible(self):
        business = Business.objects.create(
            owner=self.owner, name="Pending Shop", category=self.category,
            county=self.county, town=self.town,
        )
        response = self.client.get(business.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_approved_business_is_visible(self):
        business = Business.objects.create(
            owner=self.owner, name="Approved Shop", category=self.category,
            county=self.county, town=self.town,
            approval_status=Business.ApprovalStatus.APPROVED,
        )
        response = self.client.get(business.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_owner_can_view_own_pending_business(self):
        business = Business.objects.create(
            owner=self.owner, name="Pending Shop 2", category=self.category,
            county=self.county, town=self.town,
        )
        self.client.login(username="owner1", password="pass12345")
        response = self.client.get(business.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class SearchTests(BusinessTestBase):
    def setUp(self):
        super().setUp()
        self.business = Business.objects.create(
            owner=self.owner, name="Best Cuts Kisumu", category=self.category,
            county=self.county, town=self.town, area=self.area,
            approval_status=Business.ApprovalStatus.APPROVED,
        )

    def test_search_by_name_finds_business(self):
        response = self.client.get(reverse("businesses:list"), {"q": "Best Cuts"})
        self.assertContains(response, "Best Cuts Kisumu")

    def test_search_by_unrelated_term_finds_nothing(self):
        response = self.client.get(reverse("businesses:list"), {"q": "Nonexistent Business XYZ"})
        self.assertNotContains(response, "Best Cuts Kisumu")

    def test_filter_by_category(self):
        response = self.client.get(reverse("businesses:list"), {"category": self.category.slug})
        self.assertContains(response, "Best Cuts Kisumu")

    def test_only_approved_businesses_appear_in_search(self):
        Business.objects.create(
            owner=self.owner, name="Unapproved Shop", category=self.category,
            county=self.county, town=self.town,
        )
        response = self.client.get(reverse("businesses:list"))
        self.assertContains(response, "Best Cuts Kisumu")
        self.assertNotContains(response, "Unapproved Shop")
