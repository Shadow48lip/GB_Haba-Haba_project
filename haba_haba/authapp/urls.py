from django.urls import path
from .views import LoginAjaxView, LogoutAjaxView, RegisterAjaxView

app_name = 'auth'

urlpatterns = [
    path('register/', RegisterAjaxView.as_view(), name='register'),
    path('login/', LoginAjaxView.as_view(), name='login'),
    path('logout/', LogoutAjaxView.as_view(), name='logout'),
]
