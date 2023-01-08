from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404

from mainapp.models import CommentLike, Post, Category, Comment, PostLike, Tag, UserComplaints
from mainapp.forms import PostForm
from mainapp.utils import DataMixin, PaginatorMixin
from django.shortcuts import render


class MainappHome(DataMixin, PaginatorMixin, ListView):
    model = Post
    template_name = 'mainapp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        queryset = super().get_queryset()
        order = self.request.GET.get('order_by', '-time_create')
        return queryset.select_related(
            'author', 'cat'
        ).filter(is_published=True, is_blocked=False).order_by(order)

    # def get_ordering(self):
    #     return self.request.GET.get('order_by')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        order_query = self.request.GET.get('order_by', '-time_create')

        context['order_by'] = f"order_by={order_query}&"
        extra_context = self.get_extra_context(title='Все категории')
        paginate_context = self.get_paginate_context()
        # оператор | объединяет словари (для python 3.9+)
        context = context | extra_context | paginate_context

        # print('main:\n', context)
        return context


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'mainapp/page_post_single.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'
    queryset = Post.objects.filter(is_blocked=False, is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['read_post'] = True
        # c = Category.objects.get(slug=self.kwargs['slug'])
        context['cat_selected'] = self.object.cat.slug
        extra_context = self.get_extra_context(title=self.object.title)

        context = context | extra_context
        # counter
        self.object.total_views += 1
        self.object.save()

        # print('showpost:\n', context)
        return context


class PostsCategory(DataMixin, PaginatorMixin, ListView):
    """ Вывод статей по категориям """
    model = Post
    template_name = 'mainapp/index.html'
    context_object_name = 'post_categories'
    allow_empty = False

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related(
            'author', 'cat'
        ).filter(cat__slug=self.kwargs['slug'], is_published=True, is_blocked=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Не смысла делать этот запрос, данные уже содержаться в self.object_list
        # c = Category.objects.get(slug=self.kwargs['slug'])
        # context['cat_selected'] = c.slug
        context['cat_selected'] = self.object_list[0].cat.slug
        extra_context = self.get_extra_context(title=f'Статьи категории "{self.object_list[0].cat.name}"')
        paginate_context = self.get_paginate_context()

        context = context | extra_context | paginate_context

        # print('postcat\n', context)
        return context


class PostsTag(DataMixin, PaginatorMixin, ListView):
    """ Вывод статей по тегам """
    model = Post
    template_name = 'mainapp/index.html'
    context_object_name = 'post_tags'
    allow_empty = False

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related(
            'author', 'cat'
        ).filter(tags__slug=self.kwargs['slug'], is_published=True, is_blocked=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.get(slug=self.kwargs['slug'])
        extra_context = self.get_extra_context(title=f'Статьи по тегу #{tag.name}')
        paginate_context = self.get_paginate_context()

        context = context | extra_context | paginate_context

        # print('posttags\n', context)
        return context


class ShowComments(DataMixin, ListView):
    model = Post
    template_name = 'mainapp/page_post_single.html'
    context_object_name = 'comments'

    # allow_empty = False
    def get_queryset(self):
        queryset = super().get_queryset()
        post = Post.objects.select_related('author', 'cat').get(slug=self.kwargs['slug'])
        return queryset.select_related(
            'author', 'cat'
        ).filter(post=post, is_published=True)  # .order_by('-time_update')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.select_related('author', 'cat').get(slug=self.kwargs['slug'])
        context['post'] = post
        context['comm_count'] = Comment.get_count(post)
        context['read_post'] = False
        extra_context = self.get_extra_context(title=f'Комментарии к статье "{post.title}"')

        context = context | extra_context

        # print('showcomments\n', context)
        return context


class PostCreateView(LoginRequiredMixin, DataMixin, CreateView):
    """Создание статьи"""

    model = Post
    form_class = PostForm
    template_name = 'mainapp/page_post_create.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related(
            'author', 'cat'
        ).filter(is_published=True, is_blocked=False)  # .order_by('-time_create')

    # Добавляем автора к публикации в момент сохранения
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_extra_context(title='Новая статья')

        context = context | extra_context

        # print('postcreate\n', context)
        return context


class PostUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    """Изменение статьи"""
    model = Post
    form_class = PostForm
    template_name = 'mainapp/page_post_update.html'

    # Даём редактировать только свои статьи
    def get_object(self, **kwargs):
        return get_object_or_404(Post, pk=self.kwargs['pk'], author=self.request.user, is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_extra_context(title='Редактирование')
        context = context | extra_context
        return context


class PostDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    """Удаление статьи"""
    model = Post
    template_name = 'mainapp/page_post_delete.html'
    success_url = reverse_lazy('user:my_profile_view')

    # Даём удалять только свои статьи
    def get_object(self, **kwargs):
        return get_object_or_404(Post, pk=self.kwargs['pk'], author=self.request.user, is_deleted=False)


class AboutView(DataMixin, ListView):
    model = Post
    template_name = 'mainapp/page_about.html'

    def get_context_data(self, **kwargs):
        context = self.get_extra_context(title='О сайте')

        # print('about:\n', context)
        return context


def add_comment(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    comment = request.POST.get('text', None)
    article = request.POST.get('post', None)
    if is_ajax and article and comment:
        user = request.user
        post = get_object_or_404(Post, id=article)
        new_comment = Comment()
        new_comment.text = comment
        new_comment.user = user
        new_comment.post = post
        new_comment.is_published = True
        new_comment.save()
        return JsonResponse(
            data={
                'comment_likes_count': Comment.get_count(post),
                'id': new_comment.id,
                'data': render_to_string(
                    'mainapp/includes/_post_comment_text.html',
                    {'c': new_comment, 'user': user}
                )
            }
        )


def delete_comment(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    comment_id = request.POST.get('comment_id', None)
    if is_ajax and comment_id:
        comment = get_object_or_404(Comment, id=comment_id)
        comment.is_published = False
        comment.save()
        return JsonResponse({'result': 'ok', 'comment_id': comment_id}, status=200)


def edit_comment(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    comment_id = request.POST.get('comment_id', None)
    comment_text = request.POST.get('comment_text', None)
    if is_ajax and comment_id and comment_text:
        comment = get_object_or_404(Comment, id=comment_id)
        comment.text = comment_text
        comment.save()
        return JsonResponse({'result': 'ok', 'comment_id': comment_id}, status=200)


def like_pressed(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    comment = request.POST.get('comment', None)
    post = request.POST.get('post', None)
    if is_ajax and comment:
        comment = Comment.objects.get(id=int(comment))
        comment_add = CommentLike.set_like(comment, request.user)
        return JsonResponse(
            {
                'result': comment_add, 'object': f'comment_like_id_{comment.id}',
                'object_count': f'comment_likes_count_id_{comment.id}',
                'comment_likes_count': str(CommentLike.get_count(comment)),
                'data': render_to_string(
                    'mainapp/includes/_post_comments.html',
                    {
                        'comment': comment.id,
                        'user': request.user,
                    }
                )
            }
        )
    if is_ajax and post:
        post = Post.objects.get(id=int(post))
        post_add = PostLike.set_like(post, request.user)
        return JsonResponse(
            {
                'result': post_add, 'object': f'post_like_id_{post.id}',
                'object_count': f'post_count_id_{post.id}', 'post_like_count': str(PostLike.get_count(post)),
                'data': render_to_string(
                    'mainapp/includes/_post_likes.html',
                    {
                        'post': post,
                        'user': request.user,
                        'post_like_count': str(PostLike.get_count(post))
                    }
                )
            }
        )


def bad_comment(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    comment = request.POST.get('comment_id', None)
    post = request.POST.get('post_id', None)
    if is_ajax and comment and post:
        post = get_object_or_404(Post, id=post)
        comment = get_object_or_404(Comment, id=comment)
        complaint_add = UserComplaints.set_сomplaint(post, request.user, comment)
        return JsonResponse(
            {
                'object': str(comment.id),
                'complaint': complaint_add,
                'data': render_to_string(
                    'mainapp/includes/_post_comment_text.html',
                    {
                        'user': request.user,
                        'post': post,
                        'c': comment
                    }
                )
            },
            status=200
        )


def new_complaints(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        new_complaint_count = UserComplaints.get_new_complaints()
        return JsonResponse({'object': new_complaint_count}, status=200)

#
# def about(request):
#     return render(request, 'mainapp/page_about.html', {'title': 'О сайте'})
#
#
# def show_post(request, slug):
#     return HttpResponse('<h1>Статья</h1>')
#
#
# def site_category(request, slug):
#     return HttpResponse('<h1>Категория</h1>')
#
#
# # Обработчик не найденной страницы
# def page_not_found(request, exception):
#     return HttpResponseNotFound('<h1>Страница не найдена</h1>')
#
