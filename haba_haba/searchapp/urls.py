from django.urls import path
from .views import *

app_name = 'search'

urlpatterns = [
    path('', SearchView.as_view(), name='main'),
]

