from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import LoginAjaxView, RegisterAjaxView

app_name = 'auth'

urlpatterns = [
    path('register/', RegisterAjaxView.as_view(), name='register'),
    path('login/', LoginAjaxView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

# urlpatterns = [
#     path('register/', SignUp.as_view(), name='signup'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
# ]
