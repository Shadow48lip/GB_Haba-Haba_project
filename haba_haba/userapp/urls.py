from django.urls import path
from .views import *

app_name = 'user'


urlpatterns = [
    path('', redirect_2_profile, name='profile_redirect'),
    path('profile/', my_profile_view, name='my_profile_view'),
    path('profile/edit', my_profile_edit, name='my_profile_edit'),
    path('profile/<int:pk>', UserProfile.as_view(), name='user_profile'),
]

