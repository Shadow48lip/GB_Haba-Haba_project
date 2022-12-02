from django.http import HttpResponse
from django.shortcuts import render


def moderator_index(request):
    return HttpResponse('<h1>Модератор</h1>')
