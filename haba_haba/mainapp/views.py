from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, FormView
from mainapp.models import Post


class MainappHome(ListView):
    model = Post
    template_name = 'mainapp/index.html'
    context_object_name = 'posts'
    allow_empty = False  # Будет генерироваться ошибка, если записей в таблице нет.
    # Если мы вручную в строке браузера напишем не существующий путь


def show_post(request, slug):
    return HttpResponseNotFound('<h1>Статья</h1>')


# Обработчик не найденной страницы
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
