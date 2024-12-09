from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse

from cart.form import AddToBasketForm
from cart.models import Basket
from catalogue.models import Product


def add_to_cart_view(request):
    # Retrieve basket_id from cookies and product_id from POST
    basket_id = request.COOKIES.get("basket_id", None)
    product_id = request.POST.get("product")
    product = get_object_or_404(Product, id=product_id)

    # Attempt to retrieve the basket; create a new one if it doesn't exist
    if basket_id is None:
        basket = Basket.objects.create()
    else:
        try:
            basket = Basket.objects.get(id=basket_id)
        except Basket.DoesNotExist:
            basket = Basket.objects.create()

    # Associate the basket with the logged-in user, if authenticated
    if request.user.is_authenticated:
        if basket.user is not None and basket.user != request.user:
            raise Http404  # Prevent cross-user basket sharing
        basket.user = request.user
        basket.save()

    # Initialize and validate the form
    form = AddToBasketForm(request.POST, product_id=product.id)
    if form.is_valid():
        form.save(basket=basket)  # Add the product to the basket

    # Prepare the response and set the basket_id cookie if it was created
    response = HttpResponseRedirect(reverse("product-detail", args=[product.id]))
    if basket_id is None:
        response.set_cookie("basket_id", basket.id)

    return response
