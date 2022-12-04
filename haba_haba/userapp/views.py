from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.core.paginator import Paginator

from .models import HabaUser
from .services import get_user_posts


def redirect_2_profile(request):
    """Сервисный редирект, если кто-то зайдёт на пустую /user/"""
    response = redirect('profile/')
    return response


@login_required
def my_profile_view(request):
    """Выводит профиль авторизованного пользователя"""

    posts = get_user_posts(request.user)

    paginator = Paginator(posts, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {
        'title': 'кабинет пользователя',
        'page_obj': page_obj,
    }

    # переменная user есть во всех шаблонах и содержит авторизованного пользователя
    return render(request, 'userapp/user_cabinet.html', context=content)


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
        context['title'] = 'Профиль пользователя'
        return context




""" https://ru.stackoverflow.com/questions/1103341/Как-получить-текущего-пользователя-в-models-py """
