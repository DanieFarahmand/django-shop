from django.contrib import admin

from cart.models import Basket, BasketLine

from django.contrib import admin
from cart.models import Basket


class BasketLineInline(admin.TabularInline):
    model = BasketLine
    extra = 1
    fields = ['product', 'quantity', 'color', 'size', 'basket_user']
    readonly_fields = ['basket_user']
    autocomplete_fields = ['product', 'color', 'size']

    def basket_user(self, obj):
        """Display the user associated with the basket."""
        return obj.basket.user.id if obj.basket and obj.basket.user else "Anonymous"

    basket_user.short_description = "Basket User"


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['user', "id", 'created_time', 'updated_time']
    search_fields = ['user']
    inlines = [BasketLineInline]
    list_filter = ['user', 'created_time']


@admin.register(BasketLine)
class BasketLineAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'color', 'size',
                    'basket']  # Customize the fields you want to display in the list view
    search_fields = ['product__title', 'color__name', 'size__name']  # Allow search by product name, color, and size
    list_filter = ['product', 'color', 'size']  # Add filters for product, color, and size
