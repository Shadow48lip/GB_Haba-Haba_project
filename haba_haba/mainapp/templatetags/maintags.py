from django import template
from django.template.defaultfilters import stringfilter

from mainapp.models import Category

register = template.Library()


@register.filter(name='post_photo_process')
@stringfilter
def post_photo_process(string):
    """
    Если нет фото, то вставляет заглушку. В будущем можно добавить еще проверки.
    """
    if not string:
        string = 'https://img.freepik.com/free-vector/tiny-characters-sitting-laptop-with-lorem-ipsum-title_74855-20389.jpg?w=1480&t=st=1665865814~exp=1665866414~hmac=0dfaf49fe1350925106e58bf01a6d184411e0f59751204fabe0edcd6c2ffda63'

    return f'{string}'


@register.inclusion_tag('mainapp/includes/site_main_categories.html')
def show_main_categories(cat_selected=None):
    categories = Category.objects.all()
    return {'categories': categories, 'cat_selected': cat_selected}
