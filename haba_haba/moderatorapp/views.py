from django.http import HttpResponse
from django.shortcuts import render


def moderator_index(request):
    print(request.user.groups)
    if request.user.is_superuser:
        print('superuser')
    return HttpResponse('<h1>Модератор</h1>')


# https://qna.habr.com/q/567186