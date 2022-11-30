from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from .models import HabaUser
from mainapp.models import Post


def redirect_2_profile(request):
    response = redirect('profile/')
    return response


@login_required
def my_profile_view(request):
    """Выводит профиль авторизованного пользователя"""

    posts = get_user_posts(request.user)
    content = {
        'title': 'кабинет пользователя',
        'posts': posts,
    }

    # переменная user есть во всех шаблонах и содержит авторизованного пользователя
    return render(request, 'userapp/user_cabinet.html', content)


def my_profile_edit(request):
    """Редактирование пользователем данных о себе"""
    content = {'title': 'кабинет пользователя'}
    return render(request, 'userapp/user_edit.html', content)


class UserProfile(DetailView):
    model = HabaUser
    template_name = 'userapp/user_profile.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'профиль пользователя'
        return context


def get_user_posts(user: HabaUser):
    """Запрос статей пользователя"""
    return Post.objects.filter(author=user).values('title', 'content')

""" https://ru.stackoverflow.com/questions/1103341/Как-получить-текущего-пользователя-в-models-py """
