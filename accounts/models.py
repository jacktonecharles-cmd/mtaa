from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for MtaaBiz Kenya.

    We extend Django's built-in AbstractUser instead of writing auth
    from scratch, and add a `user_type` so the same account system
    supports both normal users and business owners. A user starts as
    a normal user and becomes a "business_owner" automatically once
    they register their first business (handled in the businesses app).
    """

    class UserType(models.TextChoices):
        NORMAL = "normal", "Normal User"
        BUSINESS_OWNER = "business_owner", "Business Owner"

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.NORMAL,
    )
    phone_number = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(
        upload_to="profile_photos/", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    @property
    def is_business_owner(self):
        return self.user_type == self.UserType.BUSINESS_OWNER
