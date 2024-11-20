import json
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from catalogue.utils import check_is_staff
from catalogue.models import Category
from django.http import HttpResponse
from .models import Product
from django.shortcuts import get_object_or_404


def product_list_view(request):
    context = {}
    products = Product.objects.all()
    context["products"] = products
    return render(request, "catalogue/product_list.html", context=context)


def homepage_view(request):
    all_products = Product.objects.all()
    newest_products = all_products.order_by("-created_time")
    context = {

        'products': all_products,
        'newest_products': newest_products,
        "most_soled": ...,
        "blog_posts": ...
    }

    return render(request, "homepage.html", context=context)


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Fetch color and size variants
    color_variants = product.attribute_values.filter(attribute__title="color variants")
    size_variants = product.attribute_values.filter(attribute__title="size variants")

    colors = [color for variant in color_variants for color in json.loads(variant.value)] if color_variants else []
    sizes = [size for variant in size_variants for size in json.loads(variant.value)] if size_variants else []

    excluded_attributes = ['color variants', 'size variants']

    context = {
        'product': product,
        'excluded_attributes': excluded_attributes,
        'colors': colors,
        'sizes': sizes,
    }

    return render(request, "catalogue/product-detail.html", context)


def category_products_view(request, pk):
    # try:
    #     category = Category.objects.get(pk=pk)
    # except Category.DoesNotExist:
    #     return HttpResponse("Category does not exist!")
    # products = Product.objects.filter(category=category)
    #
    # category.products.all()
    # 1 : select_related   2 : prefetch_related

    products = Product.objects.select_related("category").all()
    context = "\n".join([f"{p.title} - {p.category}" for p in products])
    return HttpResponse(context)


def product_search_view(request):
    query = request.GET.get("title")
    products = Product.objects.filter(
        is_active=True,
        title__icontains=query
    )


@login_required(login_url="admin/login/")
@require_http_methods(request_method_list=["GET"])
@user_passes_test(check_is_staff)
# @user_passes_test(lambda user: user.is_active, login_url="/")
@permission_required("transaction.has_score_permission")
def user_profile(request):
    return HttpResponse(f"hello {request.user.username}")
