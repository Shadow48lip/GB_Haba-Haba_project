from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, FormView
from mainapp.models import Post, Category, Comment
from mainapp.utils import DataMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect


class MainappHome(DataMixin, ListView):
    model = Post
    template_name = 'mainapp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        queryset = super(MainappHome, self).get_queryset()
        return queryset.filter(is_published=True, is_blocked=False).order_by('time_update')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        context['news'] = Post.get_new_post()
        return context


class ShowPost(DetailView):
    model = Post
    template_name = 'mainapp/includes/_post_single.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Post.objects.get(slug=self.kwargs['slug'])
        context['news'] = Post.get_new_post()
        return context


class PostCategory(DataMixin, ListView):
    model = Post
    template_name = 'mainapp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = 'Категория - ' + str(c.name)
        context['cat_selected'] = c.slug

        return context

    def get_queryset(self):
        return Post.objects.filter(cat__slug=self.kwargs['slug']).select_related('cat')


class ShowComments(DataMixin, ListView):
    model = Post
    template_name = 'mainapp/comments.html'
    context_object_name = 'comments'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(slug=self.kwargs['slug'])
        context['title'] = 'Комментарии к статье - ' + str(post.title)
        context['post'] = post
        context['comm_count'] = Comment.get_count(post)
        return context

    def get_queryset(self):
        return Comment.objects.filter(post=Post.objects.get(slug=self.kwargs['slug']), is_published=True)


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.is_published = False
    comment.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def show_post(request, slug):
    return HttpResponse('<h1>Статья</h1>')


def site_category(request, slug):
    return HttpResponse('<h1>Категория</h1>')


# Обработчик не найденной страницы
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
