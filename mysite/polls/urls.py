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
    path('leaderboards', views.leaderboards, name='leaderboards'),
    path('profile', views.profile, name='profile'),
    path('', views.home, name='home'),
    path('viewprofile/<username>', views.view_profile, name='viewprofile'),
    path('vote/<photo_id>', views.vote, name='vote'),
    path('unvote/<photo_id>', views.unvote, name='unvote'),
    path('deletephoto/<photo_id>',views.delete_photo,name='deletephoto'),
    path('deleteuser/<username>',views.delete_account,name='deleteuser'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

#set the media roots
if settings.DEBUG:
	urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
