"""This module defines the django apps in the project"""
from django.apps import AppConfig


class PollsConfig(AppConfig):
        """Configure the polls application which we are basing our web-app on"""
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'polls'
