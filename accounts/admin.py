from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username", "email", "user_type", "phone_number",
        "is_active", "is_staff", "created_at",
    )
    list_filter = ("user_type", "is_active", "is_staff")
    search_fields = ("username", "email", "phone_number")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("MtaaBiz Profile", {"fields": ("user_type", "phone_number", "profile_photo")}),
    )
