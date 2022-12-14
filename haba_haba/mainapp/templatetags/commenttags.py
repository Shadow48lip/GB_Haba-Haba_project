from django import template

from mainapp.models import Comment, CommentLike, UserComplaints

register = template.Library()


@register.simple_tag(name='comment_count')
def get_comment_count(post):
    return Comment.get_count(post)


@register.inclusion_tag('mainapp/includes/_post_comments.html', name='post_comments')
def show_comments(post, user, read_post):
    comments = Comment.objects.select_related(
        'post', 'user'
    ).filter(post=post, is_published=True).order_by('-time_create')
    comment_count = Comment.get_count(post)
    return {'comments': comments, 'user': user, 'comment_count': comment_count, 'post': post, 'read_post': read_post}


@register.simple_tag(name='comment_like_count')
def get_comment_like_count(comment):
    return CommentLike.get_count(comment)


@register.simple_tag(name='comment_liked')
def get_comment_liked(comment, user):
    if not user.is_authenticated:
        return 'bi-heart'
    return CommentLike.comment_liked(comment, user)


@register.simple_tag(name='get_user_complaint')
def get_user_complaint(comment, post, user):
    return UserComplaints.get_сomplaint(post, user, comment)
