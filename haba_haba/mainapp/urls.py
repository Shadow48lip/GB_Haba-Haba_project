from django.urls import path, re_path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', MainappHome.as_view(), name='home'),
    path('post/<slug:slug>/', ShowPost.as_view(), name='post'),
    path('cat/<slug:slug>', PostCategory.as_view(), name='category'),
    path('comments/<slug:slug>', ShowComments.as_view(), name='comment'),
    path('comment/delete/', delete_comment, name='delete_comment'),
    path('comment/add/', add_comment, name='add_comment'),
    path('comment/edit/', edit_comment, name='edit_comment'),
    path('cat/<slug:slug>/', PostCategory.as_view(), name='category'),
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    path('post/<slug:slug>', PostUpdateView.as_view(), name='post_edit'),
    path('likepress/', like_pressed, name='set_like'),
    path('post_delete/<slug:slug>/', PostDeleteView.as_view(), name='post_delete'),
]

