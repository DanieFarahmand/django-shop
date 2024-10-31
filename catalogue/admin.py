from django.contrib import admin
from catalogue.models import ProductType, Product, ProductImage, Category, Brand, ProductAttribute, \
    ProductAttributeValue


class ProductTypeAttributeInline(admin.TabularInline):
    model = ProductAttribute


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductTypeAttributeValueInline(admin.TabularInline):
    model = ProductAttributeValue
    fields = ['attribute', 'value', 'attribute_type_display']
    readonly_fields = ['attribute_type_display']

    @staticmethod
    def attribute_type_display(obj):
        if obj and obj.attribute:
            return obj.attribute.get_attribute_type_display()
        return '-'

    attribute_type_display.short_description = 'Attribute Type'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "attribute" and hasattr(request, 'object'):
            product_type = request.object.product_type
            field.queryset = ProductAttribute.objects.filter(product_type=product_type)
        return field


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductTypeAttributeInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "upc", "category", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["is_active"]
    search_fields = ["title", "upc", "category__name", "brand__name"]
    actions = ["activate_all", "deactivate_all"]
    inlines = [ProductTypeAttributeValueInline, ProductImageInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is not None:
            request.object = obj
        return form

    @staticmethod
    def activate_all(request, queryset):
        queryset.update(is_active=True)

    @staticmethod
    def deactivate_all(request, queryset):
        queryset.update(is_active=False)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
