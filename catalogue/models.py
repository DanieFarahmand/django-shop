from django.db import models


class MyModelManager(models.Model):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_active=True)


class ProductType(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    INTEGER = 1
    STRING = 2
    FLOAT = 3
    CHOICE_FIELD = (
        (INTEGER, "integer"),
        (STRING, "string"),
        (FLOAT, "float")
    )
    title = models.CharField(max_length=32)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="attributes")
    attribute_type = models.PositiveSmallIntegerField(default=INTEGER, choices=CHOICE_FIELD)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("category-detail", args=[self.pk])


class Brand(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=32)
    upc = models.BigIntegerField(unique=True)
    description = models.TextField(blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")
    is_active = models.BooleanField(default=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    custom_objects = MyModelManager()

    def __str__(self):
        return self.title

    @property
    def product_default_price(self):
        return self.partners.all().order_by("price").first()


class ProductImage(models.Model):
    image = models.ImageField(upload_to="products/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attribute_values")
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name="value")
    value = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.product} ({self.attribute}: {self.value})"
