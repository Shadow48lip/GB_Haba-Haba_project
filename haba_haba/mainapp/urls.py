from django.urls import path, re_path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', MainappHome.as_view(), name='home'),
    path('post/<slug:slug>/', ShowPost.as_view(), name='post'),
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    path('update_post/<int:pk>/', PostUpdateView.as_view(), name='edit_post'),
    path('delete_post/<int:pk>/', PostDeleteView.as_view(), name='delete_post'),

    path('comments/<slug:slug>/', ShowComments.as_view(), name='comment'),
    path('comment/delete/', delete_comment, name='delete_comment'),
    path('comment/add/', add_comment, name='add_comment'),
    path('comment/edit/', edit_comment, name='edit_comment'),

    path('category/<slug:slug>/', PostsCategory.as_view(), name='category'),
    path('tag/<slug:slug>/', PostsTag.as_view(), name='tag'),

    path('likepress/', like_pressed, name='set_like'),

    path('badcomment/', bad_comment, name='bad_comment'),
    path('newcomplaints/', new_complaints, name='new_complaints'),

    path('badpost/', bad_post, name='bad_post'),

    path('about/', AboutView.as_view(), name='about'),
    # path('update_post/<str:pk>', views.update_post, name='update_post'),
]
