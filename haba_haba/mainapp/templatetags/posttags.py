"""Теги для шаблонов, относящиеся к публикации статей"""
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.inclusion_tag('mainapp/includes/_post_mini.html', name='post_mini')
def show_post_mini(post, user):
    """Формирует оформленный с html блок привью статьи.
    @post: статья
    """

    return {'p': post, 'user': user}


@register.inclusion_tag('mainapp/includes/_post_mini_single.html', name='post_mini_single')
def show_post_mini_single(post):
    return {'p': post}


@register.filter(name='post_photo_process')
@stringfilter
def post_photo_process(string):
    """
    Если нет фото, то вставляет заглушку. В будущем можно добавить еще проверки.
    """
    if not string:
        string = 'https://img.freepik.com/free-vector/tiny-characters-sitting-laptop-with-lorem-ipsum-title_74855-20389.jpg?w=1480&t=st=1665865814~exp=1665866414~hmac=0dfaf49fe1350925106e58bf01a6d184411e0f59751204fabe0edcd6c2ffda63'

    return f'{string}'
