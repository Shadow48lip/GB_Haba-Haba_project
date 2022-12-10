from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
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


def my_profile_edit(request):
    """Редактирование пользователем данных о себе."""

    content = {'title': 'кабинет пользователя'}
    return render(request, 'userapp/user_edit.html', content)


class MyProfile(LoginRequiredMixin, DataMixin, ListView):
    """Просмотр своего профиля пользователя. Доступен только авторизованным."""

    model = Post
    template_name = 'userapp/user_cabinet.html'
    context_object_name = 'object'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Кабинет {self.request.user}')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class MyProfileUpdate(LoginRequiredMixin, DataMixin, UpdateView):
    """Редактирование профиля своего пользователя."""

    model = HabaUser
    template_name = 'userapp/user_edit.html'
    form_class = EditUserForm
    success_url = reverse_lazy('user:my_profile_view')

    # success_message = 'update success'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Редактирование {self.request.user}')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_object(self):
        return HabaUser.objects.get(pk=self.request.user.pk)

    def form_valid(self, form):
        print('qqqqqqqqqqqqqqqqqwwwwwwwwwwww')
        print(form.cleaned_data.get('password2'))

        self.object.set_password('12345')
        # pbkdf2_sha256$390000$anmb6NAplVQhjTGiIOePZI$FUOU/2tmfDea7ywzXDwg3Rgl878jyj66Z9hEBET+4ys=

        # self.object = form.save()
        return super().form_valid(form)


class UserProfile(DetailView):
    """Публичный просмотр чужого профиля пользователя."""

    model = HabaUser
    template_name = 'userapp/user_profile.html'
    context_object_name = 'object'

    # form_class = AddPostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль пользователя'
        return context


""" Полезности https://proproprogs.ru/django/mixins-ubiraem-dublirovanie-koda """
