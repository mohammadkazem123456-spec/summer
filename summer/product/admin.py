from django.contrib import admin
from .models import Product, Category, Testimonial


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "latin_name")
    search_fields = ("name", "latin_name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "show_image")
    list_filter = ("category",)
    search_fields = ("title", "subtitle")
    list_editable = ("price",)
    readonly_fields = ("preview",)

    def show_image(self, obj):
        if obj.image:
            return f"✔️"
        return "❌"

    show_image.short_description = "Image"

    # نمایش پیش‌نمایش عکس داخل صفحه ویرایش
    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height:120px; border-radius:8px;" />'
        return "No image"

    preview.allow_tags = True
    preview.short_description = "Preview"


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
