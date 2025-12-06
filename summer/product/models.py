from django.db import models

# Create your models here.
from django.db import models
from ckeditor.fields import RichTextField


def convert_farsi_to_arabic(text: str) -> str:
    """
    تبدیل کاف و ی فارسی به عربی
    """
    if not text:
        return text
    text = text.replace("ک", "ك").replace("ی", "ي")
    return text


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته")
    latin_name = models.CharField(
        max_length=100, verbose_name="نام لاتین", blank=True, null=True
    )

    def save(self, *args, **kwargs):
        self.name = convert_farsi_to_arabic(self.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان محصول")
    subtitle = models.CharField(
        max_length=300, verbose_name="زیرعنوان", blank=True, null=True
    )
    image = models.ImageField(upload_to="images/products/")
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="دسته‌بندی",
    )
    content = RichTextField(verbose_name="محتوا", blank=True, null=True)

    def save(self, *args, **kwargs):
        # قبل از ذخیره، تبدیل فارسی به عربی
        self.title = convert_farsi_to_arabic(self.title)
        if self.subtitle:
            self.subtitle = convert_farsi_to_arabic(self.subtitle)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ["-id"]

    def __str__(self):
        return self.title


# -----------------------------
# گالری تصاویر محصول
class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="gallery"
    )
    image = models.ImageField(upload_to="images/product_gallery/")
    alt_text = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="توضیح تصویر"
    )

    def __str__(self):
        return f"{self.product.title} - گالری"


# -----------------------------
# ویژگی‌ها و مشخصات محصول
class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="features"
    )
    key = models.CharField(max_length=100, verbose_name="ویژگی")
    value = models.CharField(max_length=200, verbose_name="مقدار")

    def __str__(self):
        return f"{self.product.title} - {self.key}: {self.value}"


class Testimonial(models.Model):
    RATING_CHOICES = [(i, "★" * i) for i in range(1, 6)]

    author_name = models.CharField(max_length=100, verbose_name="نام نویسنده")
    author_job = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="سمت"
    )
    quote = models.TextField(verbose_name="متن نظر")
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, default=5, verbose_name="امتیاز"
    )
    avatar = models.ImageField(
        upload_to="testimonials/avatars/", blank=True, null=True, verbose_name="آواتار"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.author_name = convert_farsi_to_arabic(self.author_name)
        self.quote = convert_farsi_to_arabic(self.quote)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "نظر مشتری"
        verbose_name_plural = "نظرات مشتریان"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author_name} - {self.rating}★"


from django.db import models


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"


from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    primary = models.CharField(
        max_length=7, default="#0a0a0a", verbose_name="اصلی"
    )  # HEX
    accent = models.CharField(max_length=7, default="#6d4677", verbose_name="متن 2")
    accent_hover = models.CharField(
        max_length=7, default="#d763a6", verbose_name="هاور متن"
    )
    text_light = models.CharField(max_length=7, default="#ffffff", verbose_name="متن")
    text_muted = models.CharField(
        max_length=7, default="#999999", verbose_name="رنگ متن توضیح "
    )
    bg_dark = models.CharField(
        max_length=7, default="#000000", verbose_name="رنگ زمینه"
    )
    bg_dark_second = models.CharField(
        max_length=7, default="#222222", verbose_name="رنگ زمینه 2"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SiteSetting(models.Model):
    about_title = models.CharField(
        max_length=255, verbose_name="عنوان معرفی", blank=True, null=True
    )
    about_description = models.TextField(
        verbose_name="توضیحات معرفی", blank=True, null=True
    )
    homepage_description = models.TextField(
        verbose_name="الرئیسیه Description", blank=True, null=True
    )
    vision = models.TextField(verbose_name="رؤيتنا", blank=True, null=True)
    location = models.CharField(
        max_length=255, verbose_name="موقعنا", blank=True, null=True
    )
    location = models.TextField(verbose_name="موقع علی الگوگل", blank=True, null=True)

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def __str__(self):
        return "تنظیمات سایت"


class PhoneNumber(models.Model):
    setting = models.ForeignKey(
        SiteSetting,
        on_delete=models.CASCADE,
        related_name="phones",
        verbose_name="تنظیمات مربوطه",
        blank=True,
        null=True,  # اجازه می‌دهد که هنگام migration رکوردهای موجود مشکل نداشته باشد
    )
    name = models.CharField(max_length=50, verbose_name="نام", blank=True, null=True)
    number = models.CharField(
        max_length=50, verbose_name="شماره تلفن", blank=True, null=True
    )

    class Meta:
        verbose_name = "شماره تلفن"
        verbose_name_plural = "شماره‌های تلفن"

    def __str__(self):
        return self.number or "بدون شماره"
