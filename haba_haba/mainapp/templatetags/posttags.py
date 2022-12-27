"""Теги для шаблонов, относящиеся к публикации статей"""
from django import template
from django.template.defaultfilters import stringfilter
from django.conf import settings

from mainapp.models import PostLike

register = template.Library()


@register.inclusion_tag('mainapp/includes/_content_post_mini.html', name='post_mini')
def show_post_mini(post, user):
    """Формирует оформленный с html блок привью статьи.
    @post: статья
    """

    return {'post': post, 'user': user}


@register.filter(name='post_photo_process')
@stringfilter
def post_photo_process(string):
    """
    Если нет фото, то вставляет заглушку. В будущем можно добавить еще проверки.
    """
    if not string:
        return f'/{settings.NO_IMAGE_URL}'

    return f'{settings.MEDIA_URL}{string}'


@register.simple_tag(name='post_like_count')
def get_post_likes_count(post):
    return PostLike.objects.filter(post=post).count()


@register.simple_tag(name='post_liked')
def get_post_liked(post, user):
    if not user.is_authenticated:
        return 'bi-heart'
    return PostLike.post_liked(post, user)
