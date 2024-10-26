from django.db import models

from catalogue.models import Product


class Partner(models.Model):
    name = models.CharField(max_length=32)
    is_active = models.BooleanField()
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class PartnerProduct(models.Model):
    partner = models.ForeignKey(Partner, related_name="products", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="partners", on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(default=0)
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} from {self.partner} : {self.price}$"
