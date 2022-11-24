from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


# Заглушка
def index(request):
    return HttpResponse('НАЧИНАЕМ HABA-HABA')


# Обработчик не найденной страницы
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
