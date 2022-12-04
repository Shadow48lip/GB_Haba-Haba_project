# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from authapp.forms import UserRegisterForm


class SignUp(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('auth:login')
    template_name = 'registration/signup.html'
