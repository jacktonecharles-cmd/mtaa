from django.contrib import admin

from .models import County, Town, Area


class TownInline(admin.TabularInline):
    model = Town
    extra = 1
    prepopulated_fields = {"slug": ("name",)}


class AreaInline(admin.TabularInline):
    model = Area
    extra = 1
    prepopulated_fields = {"slug": ("name",)}


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [TownInline]


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ("name", "county", "slug")
    list_filter = ("county",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AreaInline]


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("name", "town", "slug")
    list_filter = ("town__county", "town")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
