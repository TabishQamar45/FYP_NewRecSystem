from django.urls import path,include
from django.contrib import admin
from .views import UserRegiserView
from django.contrib.auth import views as auth_views

#URLconfg
urlpatterns=[
    path('register/',UserRegiserView.as_view(),name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='registeration/login.html'),name='login'),
]
