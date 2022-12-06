from django import template

from mainapp.models import Comment

register = template.Library()


@register.simple_tag(name='comment_count')
def get_comment_count(post):
    return Comment.get_count(post)