"""This is used to display the models in the django's admin panel."""
from django.contrib import admin
from django.utils.html import format_html

from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """This is used for looking at all the
     images saved on the database."""
    fields = ['user', 'title', 'description', 'img', 'image_tag',
              'gps_coordinates', 'taken_date', 'score']
    readonly_fields = ['user', 'title', 'description', 'img',
                       'image_tag', 'gps_coordinates', 'taken_date']
    actions = ['delete_model']

    def image_tag(self, img):
        """This is used to create a displayable image."""
        return format_html('<img src="{url}" width="150" height="150"/>'
                           .format(url=img.image.url))

    def has_add_permission(self, request, obj=None):
        """This is used to update add permissions to false."""
        return False

    def delete_model(self, request, obj):
        """Overwriting the image deletion method to allow for overwriting the image."""
        obj.title = "DELETED"
        obj.description = "This image has been deleted by an administrator."
        obj.img = "picture/error.jpg"
        obj.save()

    image_tag.short_description = 'Image'