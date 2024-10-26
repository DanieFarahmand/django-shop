from django import forms
from catalogue.models import Product, ProductAttributeValue, ProductAttribute


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            product_type = self.instance.product_type
            self.fields['attribute_values'].queryset = ProductAttributeValue.objects.filter(
                attribute__product_type=product_type
            )
        else:

            self.fields['attribute_values'].queryset = ProductAttributeValue.objects.none()


class ProductAttributeValueInlineForm(forms.ModelForm):
    class Meta:
        model = ProductAttributeValue
        fields = ['attribute', 'value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'product_type' in kwargs['initial']:
            product_type = kwargs['initial']['product_type']
            self.fields['attribute'].queryset = ProductAttribute.objects.filter(
                product_type=product_type
            )
