from django.db import models


class ProductType(models.Model):
    title = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    INTEGER = 1
    STRING = 2
    FLOAT = 3
    LIST = 4

    CHOICE_FIELD = (
        (INTEGER, "integer"),
        (STRING, "string"),
        (FLOAT, "float"),
        (LIST, "list")
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
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name='children')

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

    @classmethod
    def get_parent_categories(cls):
        return cls.objects.filter(parrent__isnull=True)


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
    # stock = models.PositiveIntegerField(default=0)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()

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


class Color(models.Model):
    name = models.CharField(max_length=20)
    hex_code = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.name}: {self.hex_code}"


class ProductColor(models.Model):
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="colors")

    def __str__(self):
        return self.color.name


class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"size is: {self.name}"


class ProductSize(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sizes")

    def __str__(self):
        return self.size.name
