from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # URL for signup
    path('', views.auth_dashboard, name='auth_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_signup/', views.user_signup, name='user_signup'),
]