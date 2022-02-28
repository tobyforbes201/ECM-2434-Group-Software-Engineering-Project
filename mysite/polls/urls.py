"""This is used to map between the URLs and views"""
from django.urls import path

from . import views

urlpatterns = [
    path('uploadimage', views.upload_image, name='uploadimage'),
    path('not_authenticated', views.not_authenticated, name='not_authenticated'),
    path('successful_upload', views.successful_upload, name='successful_upload'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('', views.home, name='home'),
]
