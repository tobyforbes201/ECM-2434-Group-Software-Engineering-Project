"""This is used to map between the URLs and views"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('uploadimage', views.upload_image, name='uploadimage'),
    path('not_authenticated', views.not_authenticated, name='not_authenticated'),
    path('successful_upload', views.successful_upload, name='successful_upload'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('feed', views.display_feed, name='feed'),
    path('', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#set the media roots
if settings.DEBUG:
	urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
