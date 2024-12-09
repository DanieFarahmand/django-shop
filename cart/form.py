from django import forms
from catalogue.models import Product, ProductSize, ProductColor


class AddToBasketForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Product",
        widget=forms.HiddenInput,
    )
    color = forms.ModelChoiceField(
        queryset=ProductColor.objects.none(),
        label="Color",
        required=False,
    )
    size = forms.ModelChoiceField(
        queryset=ProductSize.objects.none(),
        label="Size",
        required=False,
    )
    quantity = forms.IntegerField(
        min_value=1,
        label="Quantity",
        initial=1,
    )

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop("product_id", None)
        super().__init__(*args, **kwargs)
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                self.fields["color"].queryset = ProductColor.objects.filter(product=product)
                self.fields["size"].queryset = ProductSize.objects.filter(product=product)
            except Product.DoesNotExist:
                pass

    def save(self, basket):
        basket.add(
            product=self.cleaned_data.get("product"),
            quantity=self.cleaned_data.get("quantity"),
            size=self.cleaned_data.get("size"),
            color=self.cleaned_data.get("color"),
        )
