from django.urls import path
from .views import *

app_name = 'moderator'


urlpatterns = [
    path('', moderator_index, name='index'),
    path('complain/<int:pk>/', moderation_complain, name='complain'),
    path('action/post/<int:pk>/', action_post, name='action_post'),
    path('action/comnent/<int:pk>/', action_comment, name='action_comment'),
]

