from django.db import models

# Create your models here.
from django.db import models


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
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="دسته‌بندی",
    )

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
