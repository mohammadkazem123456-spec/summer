from django.contrib import admin
from .models import (
    ContactMessage,
    PhoneNumber,
    Product,
    Category,
    SiteSetting,
    Testimonial,
    Theme,
)

from django.db import models

from django.contrib import admin
from .models import Product, ProductGallery, ProductFeature
from django import forms


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "latin_name")
    search_fields = ("name", "latin_name")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "author_name",
        "author_job",
        "rating",
        "created_at",
        "avatar_preview",
    )
    list_filter = ("rating", "created_at")
    search_fields = ("author_name", "quote")
    readonly_fields = ("avatar_preview",)

    # پیش‌نمایش آواتار در admin
    def avatar_preview(self, obj):
        if obj.avatar:
            return f'<img src="{obj.avatar.url}" style="height:50px; border-radius:50%;" />'
        return "-"

    avatar_preview.allow_tags = True
    avatar_preview.short_description = "آواتار"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "subject", "created_at")
    list_filter = ("created_at",)
    search_fields = ("first_name", "last_name", "email", "subject", "message")
    readonly_fields = ("created_at",)


class ThemeAdminForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = "__all__"
        widgets = {
            "primary": forms.TextInput(attrs={"type": "color"}),
            "accent": forms.TextInput(attrs={"type": "color"}),
            "accent_hover": forms.TextInput(attrs={"type": "color"}),
            "text_light": forms.TextInput(attrs={"type": "color"}),
            "text_muted": forms.TextInput(attrs={"type": "color"}),
            "bg_dark": forms.TextInput(attrs={"type": "color"}),
            "bg_dark_second": forms.TextInput(attrs={"type": "color"}),
        }


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    form = ThemeAdminForm
    list_display = ("name", "primary", "accent", "accent_hover")


class PhoneInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    inlines = [PhoneInline]


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "show_image")
    list_filter = ("category",)
    search_fields = ("title", "subtitle")
    list_editable = ("price",)
    readonly_fields = ("preview",)
    inlines = [ProductGalleryInline, ProductFeatureInline]

    # نمایش آیکون تصویر
    def show_image(self, obj):
        if obj.image:
            return "✔️"
        return "❌"

    show_image.short_description = "Image"

    # پیش‌نمایش تصویر در صفحه ویرایش
    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height:120px; border-radius:8px;" />'
        return "No image"

    preview.allow_tags = True
    preview.short_description = "Preview"
