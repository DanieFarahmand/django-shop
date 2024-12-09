from django.urls import path

from cart.views import add_to_cart_view

urlpatterns = [
    path("add/", add_to_cart_view, name="add-to-cart")

]
