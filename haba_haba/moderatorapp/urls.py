from django.urls import path
from .views import *

app_name = 'moderator'


urlpatterns = [
    path('', moderator_index, name='index'),
    path('complain/<int:pk>/', moderation_complain, name='complain'),
    path('action/post/<int:pk>/', moderator_index, name='action_post'),
    path('action/comnet/<int:pk>/', moderator_index, name='action_comment'),
]

