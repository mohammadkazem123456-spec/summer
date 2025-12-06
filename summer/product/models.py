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
    name = models.CharField(max_length=100, verbose_name="اسم التصنيف")
    latin_name = models.CharField(
        max_length=100, verbose_name="الاسم اللاتيني", blank=True, null=True
    )

    def save(self, *args, **kwargs):
        self.name = convert_farsi_to_arabic(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "تصنيف"
        verbose_name_plural = "التصنيفات"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان المنتج")
    subtitle = models.CharField(
        max_length=300, verbose_name="العنوان الفرعي", blank=True, null=True
    )
    image = models.ImageField(upload_to="images/products/", verbose_name="الصورة")
    price = models.PositiveIntegerField(verbose_name="السعر (تومان)")
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="التصنيف",
    )
    content = RichTextField(verbose_name="المحتوى", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.title = convert_farsi_to_arabic(self.title)
        if self.subtitle:
            self.subtitle = convert_farsi_to_arabic(self.subtitle)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ["-id"]

    def __str__(self):
        return self.title


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="gallery", verbose_name="المنتج"
    )
    image = models.ImageField(
        upload_to="images/product_gallery/", verbose_name="صورة المعرض"
    )
    alt_text = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="نص بديل للصورة"
    )

    class Meta:
        verbose_name = "صورة المعرض"
        verbose_name_plural = "معرض صور المنتج"

    def __str__(self):
        return f"{self.product.title} - صورة"


class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="المنتج",
    )
    key = models.CharField(max_length=100, verbose_name="الميزة")
    value = models.CharField(max_length=200, verbose_name="القيمة")

    class Meta:
        verbose_name = "ميزة"
        verbose_name_plural = "مميزات المنتج"

    def __str__(self):
        return f"{self.product.title} - {self.key}: {self.value}"


class Testimonial(models.Model):
    RATING_CHOICES = [(i, "★" * i) for i in range(1, 6)]

    author_name = models.CharField(max_length=100, verbose_name="اسم الكاتب")
    author_job = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="الوظيفة"
    )
    quote = models.TextField(verbose_name="نص التقييم")
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES, default=5, verbose_name="التقييم"
    )
    avatar = models.ImageField(
        upload_to="testimonials/avatars/",
        blank=True,
        null=True,
        verbose_name="الصورة الشخصية",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    def save(self, *args, **kwargs):
        self.author_name = convert_farsi_to_arabic(self.author_name)
        self.quote = convert_farsi_to_arabic(self.quote)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "تقييم"
        verbose_name_plural = "تقييمات العملاء"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author_name} - {self.rating}★"


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="الاسم الأول")
    last_name = models.CharField(max_length=50, verbose_name="اسم العائلة")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    subject = models.CharField(max_length=100, verbose_name="الموضوع")
    message = models.TextField(verbose_name="الرسالة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإرسال")

    class Meta:
        verbose_name = "رسالة تواصل"
        verbose_name_plural = "رسائل التواصل"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="اسم الثيم")
    primary = models.CharField(
        max_length=7, default="#0a0a0a", verbose_name="اللون الأساسي"
    )
    accent = models.CharField(
        max_length=7, default="#6d4677", verbose_name="لون النص الثاني"
    )
    accent_hover = models.CharField(
        max_length=7, default="#d763a6", verbose_name="لون الهوفر"
    )
    text_light = models.CharField(
        max_length=7, default="#ffffff", verbose_name="لون النص"
    )
    text_muted = models.CharField(
        max_length=7, default="#999999", verbose_name="لون النص الثانوي"
    )
    bg_dark = models.CharField(max_length=7, default="#000000", verbose_name="خلفية 1")
    bg_dark_second = models.CharField(
        max_length=7, default="#222222", verbose_name="خلفية 2"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    class Meta:
        verbose_name = "ثيم"
        verbose_name_plural = "الثيمات"

    def __str__(self):
        return self.name


class SiteSetting(models.Model):
    about_title = models.CharField(
        max_length=255, verbose_name="عنوان التعريف", blank=True, null=True
    )
    about_description = models.TextField(
        verbose_name="وصف التعريف", blank=True, null=True
    )
    homepage_description = models.TextField(
        verbose_name="وصف الصفحة الرئيسية", blank=True, null=True
    )
    vision = models.TextField(verbose_name="رؤيتنا", blank=True, null=True)
    location = models.TextField(
        verbose_name="موقعنا على الخرائط", blank=True, null=True
    )

    class Meta:
        verbose_name = "إعدادات الموقع"
        verbose_name_plural = "إعدادات الموقع"

    def __str__(self):
        return "إعدادات الموقع"


class PhoneNumber(models.Model):
    setting = models.ForeignKey(
        SiteSetting,
        on_delete=models.CASCADE,
        related_name="phones",
        verbose_name="الإعدادات المرتبطة",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=50, verbose_name="الاسم", blank=True, null=True)
    number = models.CharField(
        max_length=50, verbose_name="رقم الهاتف", blank=True, null=True
    )

    class Meta:
        verbose_name = "رقم هاتف"
        verbose_name_plural = "أرقام الهاتف"

    def __str__(self):
        return self.number or "بدون رقم"
