from django.contrib.auth.models import User
from django.db import models

from catalogue.models import Product, ProductColor, ProductSize


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="basket", null=True,
        blank=True
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"basket for: {self.user}"

    def add(self, product, quantity, color=None, size=None):
        # Check if the product, color, and size are valid before creating a BasketLine
        if not product:
            raise ValueError("Product cannot be null.")
        basket_line = BasketLine.objects.create(
            basket=self,
            product=product,
            quantity=quantity,
            color=color,  # Assign the selected color (can be None)
            size=size,  # Assign the selected size (can be None)
        )
        return basket_line


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="basket_lines")
    quantity = models.PositiveSmallIntegerField(default=1)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} )"
