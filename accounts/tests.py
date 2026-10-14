from django.test import TestCase
from django.urls import reverse

from .models import User


class RegistrationLoginTests(TestCase):
    def test_registration_creates_user_and_logs_in(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "janedoe",
            "email": "jane@example.com",
            "phone_number": "0700000000",
            "password1": "S3cure-Pass!23",
            "password2": "S3cure-Pass!23",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="janedoe").exists())
        # Should be logged in immediately after registering.
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        User.objects.create_user(username="bob", password="pass12345")
        response = self.client.post(reverse("accounts:login"), {
            "username": "bob", "password": "pass12345",
        })
        self.assertEqual(response.status_code, 302)

    def test_login_with_invalid_credentials_fails(self):
        User.objects.create_user(username="bob", password="pass12345")
        response = self.client.post(reverse("accounts:login"), {
            "username": "bob", "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)  # re-renders form with errors
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_profile_requires_login(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
