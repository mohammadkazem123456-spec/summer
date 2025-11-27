from django.shortcuts import render

from product.models import Category, Product, Testimonial
from django.views.decorators.cache import cache_page

# Create your views here.


@cache_page(60 * 15)  # 15 دقیقه
def home(request):
    products = Product.objects.select_related("category").all()
    categories = Category.objects.all()

    testimonials = Testimonial.objects.all()
    data = {
        "products": products,
        "categories": categories,
        "testimonials": testimonials,
    }
    return render(request, "index.html", context=data)
