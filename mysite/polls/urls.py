"""This is used to map between the URLs and views"""
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('', views.home, name='home'),
]
