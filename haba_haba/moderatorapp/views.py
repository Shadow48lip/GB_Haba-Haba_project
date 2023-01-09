from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


def moderator_index(request):
    if not request.user.is_staff:
        raise PermissionDenied()

    return HttpResponse('<h1>Модератор</h1>')



# https://qna.habr.com/q/567186