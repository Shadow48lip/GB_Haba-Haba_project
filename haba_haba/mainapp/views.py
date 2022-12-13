from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404

from mainapp.models import CommentLike, Post, Category, Comment, PostLike
from mainapp.forms import PostForm
from mainapp.utils import DataMixin


class MainappHome(DataMixin, ListView):
    model = Post
    template_name = 'mainapp/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True, is_blocked=False).order_by('time_update')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'
        context['news'] = Post.get_new_post()

        context['posts'] = Post.objects.all()
        paginator = Paginator(context['posts'], 5)
        page = self.request.GET.get('page')

        try:
            context['posts'] = paginator.page(page)
        except PageNotAnInteger:
            context['posts'] = paginator.page(1)
        except EmptyPage:
            context['posts'] = paginator.page(paginator.num_pages)

        return context


class ShowPost(DetailView):
    model = Post
    template_name = 'mainapp/includes/_post_single.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        # context['title'] = Post.objects.get(slug=self.kwargs['slug'])
        context['read_post'] = True
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


class ShowComments(ListView):
    model = Post
    template_name = 'mainapp/includes/_post_single.html'
    context_object_name = 'comments'

    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(slug=self.kwargs['slug'])
        context['title'] = 'Комментарии к статье - ' + str(post.title)
        context['post'] = post
        context['comm_count'] = Comment.get_count(post)
        context['read_post'] = False
        return context

    def get_queryset(self):
        return Comment.objects.filter(post=Post.objects.get(slug=self.kwargs['slug']), is_published=True).order_by(
            '-time_update')


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
            {'result': Comment.get_count(post),
             'data': render_to_string('mainapp/includes/_comment_text.html', {'c': new_comment, 'user': user})})


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


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'mainapp/create_post.html'


def like_pressed(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    comment = request.POST.get('comment', None)
    post = request.POST.get('post', None)
    if is_ajax and comment:
        comment = Comment.objects.get(id=int(comment))
        comment_add = CommentLike.set_like(comment, request.user)
        return JsonResponse(
            {'result': comment_add, 'object': f'comment_like_id_{comment.id}',
             'odject_count': f'comment_count_id_{comment.id}', 'comment_count': str(CommentLike.get_count(comment)),
             'data': render_to_string('mainapp/includes/_comments.html',
                                      {'comment': comment.id, 'user': request.user, })})
    if is_ajax and post:
        post = Post.objects.get(id=int(post))
        post_add = PostLike.set_like(post, request.user)
        return JsonResponse(
            {'result': post_add, 'object': f'post_like_id_{post.id}',
             'odject_count': f'post_count_id_{post.id}', 'post_like_count': str(PostLike.get_count(post)),
             'data': render_to_string('mainapp/includes/_likes.html',
                                      {'post': post, 'user': request.user,
                                       'post_like_count': str(PostLike.get_count(post))})})


def show_post(request, slug):
    return HttpResponse('<h1>Статья</h1>')


def site_category(request, slug):
    return HttpResponse('<h1>Категория</h1>')


# Обработчик не найденной страницы
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
