# URLS for autocross
from django.urls import path
from . import views

app_name = 'autocross'

urlpatterns = [
    path('', views.home, name='home'),
    path('user_profile/',  views.user_profile, name = 'user_profile'),
    path('signup/', views.SignUpView.as_view(),name = 'signup'),
    path('analytics/', views.analytics,name = 'analytics'),    
    path('all_events', views.all_events, name = 'all_events'),
]