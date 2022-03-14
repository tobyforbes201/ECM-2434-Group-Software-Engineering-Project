"""This is used for creating the schema to the database."""
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage

image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/feed/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}feed/'.format(settings.MEDIA_URL),
)

def image_directory_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/feed/picture/<filename>."""
    return u'picture/{0}'.format(filename)

class Image(models.Model):
    """A model used to store images and other related information."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    img = models.ImageField(upload_to=image_directory_path, storage=image_storage)
    gps_coordinates = models.CharField(max_length=200)
    taken_date = models.DateTimeField()
    score = models.IntegerField()

    class Meta():
        """The meta information for the Image class."""
        db_table = "polls_image"
