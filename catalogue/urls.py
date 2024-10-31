from django.urls import path
from catalogue.views import product_list_view, home_view, user_profile, category_products_view, product_detail_view, \
    product_search_view

urlpatterns = [
    path("product/list/", product_list_view, name="product-list"),
    path("category/<int:pk>/products/", category_products_view, name="category-products"),
    path("product/<int:pk>/", product_detail_view, name="product-detail"),
    path("product/search/", product_search_view, name="product-search"),
    path("profile/", user_profile, name="user-profile"),

]
