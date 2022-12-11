from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from mainapp.models import Post
from .models import HabaUser
from .utils import DataMixin
from .forms import EditUserForm


def redirect_2_profile(request):
    """Сервисный редирект, если кто-то зайдёт на пустую /user/"""
    response = redirect('profile/')
    return response


class MyProfile(LoginRequiredMixin, DataMixin, ListView):
    """Просмотр пользователем своего профиля. Доступен только авторизованным."""

    # LoginRequiredMixin отправит сюда пользователя без авторизации
    login_url = reverse_lazy('main:home')

    model = Post
    template_name = 'userapp/user_cabinet.html'
    context_object_name = 'object'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(user=self.request.user, title=f'Кабинет {self.request.user}')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class MyProfileUpdate(LoginRequiredMixin, DataMixin, UpdateView):
    """Редактирование пользователем данных о себе."""

    # LoginRequiredMixin отправит сюда пользователя без авторизации
    login_url = reverse_lazy('main:home')

    model = HabaUser
    template_name = 'userapp/user_edit.html'
    form_class = EditUserForm
    success_url = reverse_lazy('user:my_profile_view')

    # success_message = 'update success'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(user=self.request.user, title=f'Редактирование {self.request.user}')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_object(self):
        return HabaUser.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        # замена пароля
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        if password1 and password2 and password1 == password2:
            self.object.set_password(password1)
            print('пароль изменен')

        return super().form_valid(form)


class UserProfileList(DataMixin, ListView):
    """Публичный профиль пользователя. Доступен всем."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None

    model = Post
    template_name = 'userapp/user_profile.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(user=self.user, title=f'Кабинет {self.user.username}', object_user=self.user)
        context = dict(list(context.items()) + list(c_def.items()))

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.user = get_object_or_404(HabaUser, slug=self.kwargs['slug'])
        return queryset.filter(is_published=True, is_blocked=False, author=HabaUser.objects.get(slug=self.user)) \
            .order_by('time_update')


""" Полезности https://proproprogs.ru/django/mixins-ubiraem-dublirovanie-koda """
