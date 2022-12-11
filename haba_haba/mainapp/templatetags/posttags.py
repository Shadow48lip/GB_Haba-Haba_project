"""Теги для шаблонов, относящиеся к публикации статей"""
from django import template
from django.template.defaultfilters import stringfilter

from mainapp.models import PostLike

register = template.Library()


@register.inclusion_tag('mainapp/includes/_post_mini.html', name='post_mini')
def show_post_mini(post, user):
    """Формирует оформленный с html блок привью статьи.
    @post: статья
    """

    return {'p': post, 'user': user}


@register.filter(name='post_photo_process')
@stringfilter
def post_photo_process(string):
    """
    Если нет фото, то вставляет заглушку. В будущем можно добавить еще проверки.
    """
    if not string:
        string = 'https://img.freepik.com/free-vector/tiny-characters-sitting-laptop-with-lorem-ipsum-title_74855-20389.jpg?w=1480&t=st=1665865814~exp=1665866414~hmac=0dfaf49fe1350925106e58bf01a6d184411e0f59751204fabe0edcd6c2ffda63'

    return f'{string}'


@register.simple_tag(name='post_like_count')
def get_post_likes_count(post):
    return PostLike.objects.filter(post=post).count()


@register.simple_tag(name='post_liked')
def get_post_liked(post, user):
    if not user.is_authenticated:
        return 'bi-heart'
    return PostLike.post_liked(post, user)
