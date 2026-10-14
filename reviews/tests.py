from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from categories.models import Category
from locations.models import County, Town

from businesses.models import Business
from .models import Review


class ReviewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.get_or_create(name="Barbers")[0]
        self.county = County.objects.get_or_create(name="Kisumu County")[0]
        self.town = Town.objects.get_or_create(county=self.county, name="Kisumu")[0]
        self.owner = User.objects.create_user(username="owner1", password="pass12345")
        self.customer = User.objects.create_user(username="cust1", password="pass12345")
        self.business = Business.objects.create(
            owner=self.owner, name="Best Cuts", category=self.category,
            county=self.county, town=self.town,
            approval_status=Business.ApprovalStatus.APPROVED,
        )

    def test_logged_in_user_can_leave_review(self):
        self.client.login(username="cust1", password="pass12345")
        response = self.client.post(
            reverse("reviews:add", args=[self.business.id]),
            {"rating": 5, "comment": "Great!"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.filter(business=self.business, user=self.customer).count(), 1)

    def test_average_rating_calculated_correctly(self):
        Review.objects.create(business=self.business, user=self.customer, rating=4)
        second = User.objects.create_user(username="cust2", password="pass12345")
        Review.objects.create(business=self.business, user=second, rating=2)
        self.assertEqual(self.business.average_rating, 3.0)

    def test_duplicate_review_updates_instead_of_creating(self):
        self.client.login(username="cust1", password="pass12345")
        self.client.post(reverse("reviews:add", args=[self.business.id]), {"rating": 3, "comment": "OK"})
        self.client.post(reverse("reviews:add", args=[self.business.id]), {"rating": 5, "comment": "Actually great"})
        reviews = Review.objects.filter(business=self.business, user=self.customer)
        self.assertEqual(reviews.count(), 1)
        self.assertEqual(reviews.first().rating, 5)

    def test_owner_cannot_review_own_business(self):
        self.client.login(username="owner1", password="pass12345")
        self.client.post(reverse("reviews:add", args=[self.business.id]), {"rating": 5, "comment": "!"})
        self.assertEqual(Review.objects.filter(business=self.business, user=self.owner).count(), 0)
