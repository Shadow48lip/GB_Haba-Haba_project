from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from mainapp.models import Post


class DataMixin:
    @staticmethod
    def get_extra_context(**kwargs):
        context = kwargs
        context['news'] = Post.get_new_post()

        return context


class PaginatorMixin:
    def get_paginate_context(self, **kwargs):
        context = kwargs

        # пагинация для ajax
        context['posts'] = self.object_list
        context['posts'].filter(is_published=True, is_blocked=False).order_by('-time_create')
        paginator = Paginator(context['posts'], per_page=5, orphans=1)
        page = self.request.GET.get('page')

        try:
            context['posts'] = paginator.page(page)
        except PageNotAnInteger:
            context['posts'] = paginator.page(1)
        except EmptyPage:
            context['posts'] = paginator.page(paginator.num_pages)

        # print('paginatemixin:\n', context)
        return context