from django.urls import include, path
from .views import SignUp

app_name = 'auth'

urlpatterns = [
    path('register/', SignUp.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
]
