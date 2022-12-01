""" Служебные функции, которые могут понадобиться во многих местах. Бизнес логика. """
from mainapp.models import Post


def get_user_posts(user: object) -> Post:
    """Запрос статей пользователя"""
    # если надо запросить не все колонки values('title', 'content', 'slug')

    return Post.objects.filter(author=user)
