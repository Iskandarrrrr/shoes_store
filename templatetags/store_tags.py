from django import template
from store.models import Category, FavouriteProducts

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter(parent=True)


@register.simple_tag()
def get_categories_parent():
    return Category.objects.filter(parent=None)


@register.simple_tag()
def get_subcategories(category):
    return Category.objects.filter(parent=category)


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': 'Narxi',
            'sorters': [
                ('-price', 'Qimmatlari'),
                ('price', 'Arzonroq'),
            ]
        },

        {
            'title': 'Ranglar',
            'sorters': [
                ('color', 'A - Z'),
                ('color', 'Z - A'),
            ]
        },
        {
            'title': 'O`lchami',
            'sorters': [
                ('size', 'Kichiklari'),
                ('-size', 'Kattalari'),
            ]
        }
    ]
    return sorters


@register.simple_tag()
def get_favourite_products(user):
    fav = FavouriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products
