from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from mainapp.models import Post, UserComplaints

"""
как работают разрешения в Django
https://webdevblog.ru/chto-nuzhno-znat-chtoby-upravlyat-polzovatelyami-v-django-admin/
"""


def moderator_index(request):
    if not request.user.is_staff:
        raise PermissionDenied()

    content = {'title': 'Модератор', 'last_posts': Post.get_new_post()}

    # new_complains = UserComplaints.objects.select_related('post', 'user', 'comment') \
    #     .filter(moderator_id__isnull=True)
    new_complains = UserComplaints.objects.filter(moderator_id__isnull=True)
    content['new_complains'] = new_complains

    return render(request, 'moderatorapp/moder_index.html', context=content)

# https://qna.habr.com/q/567186
