from django.urls import path
from .views import *

app_name = 'moderator'


urlpatterns = [
    path('', moderator_index, name='index'),
]

