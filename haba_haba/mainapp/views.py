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
    paginate_by = 5

    def get_queryset(self):
        queryset = super(MainappHome, self).get_queryset()
        return queryset.filter(is_published=True, is_blocked=False).order_by('time_update')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        context['news'] = Post.get_new_post()
        context['single_page'] = False
        return context


class ShowPost(DetailView):
    model = Post
    template_name = 'mainapp/post.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статья'
        context['news'] = Post.get_new_post()
        context['single_page'] = True
        return context


def show_post(request, slug):
    return HttpResponse('<h1>Статья</h1>')


def site_category(request, slug):
    return HttpResponse('<h1>Категория</h1>')


# Обработчик не найденной страницы
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
