from django import template

from catalogue.models import Category

register = template.Library()


@register.simple_tag
def get_category():
    categories = Category.objects.filter(parent__isnull=True).prefetch_related(
        'children__children'
    )
    return categories
