from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', MainappHome.as_view(), name='home'),
]
