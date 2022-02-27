"""This is used for creating the schema to the database."""
from django.db import models
from django.conf import settings


class Image(models.Model):
    """A model used to store images and other related information."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    img = models.ImageField(upload_to="images/")
    gps_coordinates = models.CharField(max_length=200)
    taken_date = models.DateTimeField()
    score = models.IntegerField()
