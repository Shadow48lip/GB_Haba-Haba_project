from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.shortcuts import render

from authapp.forms import UserRegisterForm


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class RegisterAjaxView(CreateView):
    template_name = 'mainapp/includes/_modal_registration.html'

    def get(self, request, **kwargs):
        context = {
            'form': UserRegisterForm()
        }
        return render(
            request=request,
            template_name=self.template_name,
            context=context,
        )

    def post(self, request, **kwargs):
        form = UserRegisterForm(request.POST)

        if is_ajax(request):
            if form.is_valid():
                form.save()
                user = authenticate(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password1'),
                )

                if user:
                    login(
                        request=request,
                        user=user,
                    )
                    return JsonResponse(
                        data={
                            'status': 201,
                        },
                        status=200,
                    )

            elif request.POST.get('password1') != request.POST.get('password2'):
                return JsonResponse(
                    data={
                        'error': 'Пароли не совпадают!',
                        'status': 400,
                    },
                    status=200,
                )

            elif not request.POST.get('check'):
                return JsonResponse(
                    data={
                        'error': 'Необходимо согласиться с нашими правилами!',
                        'status': 400,
                    },
                    status=200,
                )

            elif not request.POST.get('username') or request.POST.get('email'):
                return JsonResponse(
                    data={
                        'error': 'Необходимо заполнить все поля!',
                        'status': 400,
                    },
                    status=200,
                )

        context = {'form': form}
        return render(
            request=request,
            template_name=self.template_name,
            context=context,
        )


class LoginAjaxView(LoginView):
    template_name = 'mainapp/includes/_modal_login.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if is_ajax(request):
            if username and password:
                user = authenticate(
                    request,
                    username=username,
                    password=password
                )

                if user:
                    login(request, user)
                    return JsonResponse(
                        data={
                            'status': 201,
                        },
                        status=200,
                    )
                return JsonResponse(
                    data={
                        'error': 'Неверный логин или пароль!',
                        'status': 400,
                    },
                    status=200,
                )
            return JsonResponse(
                data={
                    'error': 'Введите логин и пароль!',
                    'status': 400,
                },
                status=200,
            )


class LogoutAjaxView(LogoutView):
    def post(self, request, *args, **kwargs):
        if is_ajax(request):
            logout(request)
            return JsonResponse(
                data={
                    'status': 201,
                },
                status=200,
            )
