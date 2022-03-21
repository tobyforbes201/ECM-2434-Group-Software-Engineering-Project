"""This is used for creating the schema to the database."""
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from PIL import Image as PilImage

image_storage = FileSystemStorage(
    # Physical file location ROOT
    location=u'{0}/feed/'.format(settings.MEDIA_ROOT),
    # Url for file
    base_url=u'{0}feed/'.format(settings.MEDIA_URL),
)


def image_directory_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/feed/picture/<filename>."""
    return u'picture/{0}'.format(filename)


class Challenge(models.Model):
    """A model used to store challenges"""
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    locationRadius = models.IntegerField()
    subject = models.CharField(max_length=200)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()


class Badge(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="owner")
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    badge_image = models.ImageField(upload_to=image_directory_path, storage=image_storage)


class Image(models.Model):
    """A model used to store images and other related information."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    img = models.ImageField(upload_to=image_directory_path, storage=image_storage)
    gps_coordinates = models.CharField(max_length=200)
    taken_date = models.DateTimeField()
    score = models.IntegerField()
    user_votes = models.ManyToManyField(User)

    class Meta:
        """The meta information for the Image class."""
        db_table = "polls_image"


class Profile(models.Model):
    """A model to store user profiles"""
    # delete profile if user is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(default='default.jpg', upload_to=image_directory_path,
                            storage=image_storage)

    def __str__(self):
        """Used to display the profile model"""
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """Overwrite the profile image and resize it"""
        super(Profile, self).save(*args, **kwargs)

        img = PilImage.open(self.img.path)  # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)  # Resize image
            img.save(self.img.path)  # Save it again and override the larger image


class Vote(models.Model):
    """A user's vote for a photo"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="images")
    already_voted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} voted for {self.image}"
