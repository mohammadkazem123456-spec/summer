from django.shortcuts import render
from django.http import JsonResponse
from product.form import ContactForm
from product.models import Category, Product, SiteSetting, Testimonial, Theme
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# @cache_page(60 * 15)  # 15 دقیقه
def home(request):
    products = Product.objects.select_related("category").all()
    settings = SiteSetting.objects.prefetch_related("phones").first()
    categories = Category.objects.all()

    testimonials = Testimonial.objects.all()
    data = {
        "products": products,
        "categories": categories,
        "testimonials": testimonials,
        "settings": settings,
    }
    return render(request, "index.html", context=data)


@csrf_exempt  # اگر از CSRF token در JS استفاده نمی‌کنید
def contact_ajax(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "message": "تم إرسال الرسالة! ✓"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    return JsonResponse({"status": "error", "message": "طلب غير صالح"}, status=400)


from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True)
def theme_css(request):
    theme = Theme.objects.first()

    # مقادیر پیش‌فرض
    default_theme = {
        "primary": "#0a0a0a",
        "accent": "#6d4677",
        "accent_hover": "#d763a6",
        "text_light": "#ffffff",
        "text_muted": "#999",
        "bg_dark": "#000",
        "bg_dark_second": "#222",
    }

    # اگر theme موجود نبود از پیش‌فرض استفاده کن
    theme_context = theme if theme else default_theme

    return render(
        request, "css/theme.css", {"theme": theme_context}, content_type="text/css"
    )
