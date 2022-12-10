from django.urls import path
from .views import *

app_name = 'user'


urlpatterns = [
    path('', redirect_2_profile, name='profile_redirect'),
    path('profile/', MyProfile.as_view(), name='my_profile_view'),
    # path('profile/edit/', my_profile_edit, name='my_profile_edit'),
    path('profile/edit/', MyProfileUpdate.as_view(), name='my_profile_edit'),
    path('profile/<slug:slug>/', UserProfile.as_view(), name='user_profile'),
]

