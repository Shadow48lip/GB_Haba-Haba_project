from django import template

from mainapp.models import Category

register = template.Library()


@register.inclusion_tag('mainapp/includes/site_main_categories.html', name='main_categories')
def show_main_categories(cat_selected=None):
    """Меню с главными категориями сайта.
    @cat_selected: slug выбранной категории для выделения в меню.
    """
    categories = Category.objects.all()
    return {'categories': categories, 'cat_selected': cat_selected}


