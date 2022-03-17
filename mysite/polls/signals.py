"""This module signals to django that every new user needs a profile"""
from django.db.models.signals import post_save #Import a post_save signal when a user is created
from django.contrib.auth.models import User # Import the built-in User model, which is a sender
from django.dispatch import receiver # Import the receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	"""When a user is created, create a profile"""
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	"""When the profile is created, save it"""
	instance.profile.save()
	