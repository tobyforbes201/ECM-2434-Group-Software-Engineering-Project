from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uploadimage', views.upload_image, name='uploadimage'),
    path('not_authenticated', views.not_authenticated, name='not_authenticated'),
    path('successful_upload', views.successful_upload, name='auccessful_upload'),
]
