from django.db.models import Q
from django.views.generic import ListView

from mainapp.models import Post
from mainapp.utils import DataMixin, PaginatorMixin


class SearchView(DataMixin, PaginatorMixin, ListView):
    template_name = 'mainapp/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        search_query = self.request.GET.get('q')
        queryset = Post.objects.select_related(
            'cat', 'author'
        ).filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        ).filter(is_published=True, is_blocked=False)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_query = self.request.GET.get('q')

        context['q'] = f"q={search_query}&"
        extra_context = self.get_extra_context(title=f'Результаты поиска по запросу "{search_query}"')
        paginate_context = self.get_paginate_context()

        context = context | extra_context | paginate_context

        print('search:\n', context)
        return context
