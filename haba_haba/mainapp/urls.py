from django.urls import path, re_path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', MainappHome.as_view(), name='home'),
    path('post/<slug:slug>/', ShowPost.as_view(), name='post'),
    path('cat/<slug:slug>', PostCategory.as_view(), name='category'),
    path('comments/<slug:slug>', ShowComments.as_view(), name='comment'),
    path('comment/delete/<int:pk>', delete_comment, name='delete_comment'),
]

