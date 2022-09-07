# URLS for autocross
from django.urls import path
from . import views

app_name = 'autocross'

urlpatterns = [
    path('', views.home, name='home'),
    path('user_profile/',  views.user_profile, name = 'user_profile')
]