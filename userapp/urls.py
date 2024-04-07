from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('registration/', registration, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='userapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('profile/', profile, name='all_profile'),
    path('profileupdate/', profileupdate, name='p_update'),
    path('password_change/', login_required(auth_views.PasswordChangeView.as_view(template_name='userapp/password_change.html'), login_url='login'), name='password_change'),
    path('password_change_done/', login_required(auth_views.PasswordChangeDoneView.as_view(template_name='userapp/password_change_done.html'), login_url='login'), name='password_change_done'),
]
  
