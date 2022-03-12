"""This is used for functions that validate values in forms."""

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime
from exif import Image
import os


def check_user_unique(username):
    """This function will check if a username entered is unique
    and is not the same as an existing user."""
    if User.objects.filter(username=username).exists():
        raise ValidationError(f"Username {username} is already taken.", params={'value': username},
                              code='user_not_unique')


def validate_number(password):
    """This function will check if there are only letters or special characters in the password,
    raising an error if that is true."""
    if password.isalpha():
        raise ValidationError("Password does not contain any numbers.",
                              code='password_no_numbers')


def validate_special(password):
    """This function will check if there are only letters or number in the password,
    raising an error if that is true."""
    if password.isalnum():
        raise ValidationError("Password does not contain any special characters.",
                              code='password_no_special_char')


def validate_upper_lower(password):
    """This function will check if the password contains all lower case or all upper case letters,
    raising an error if either are true."""
    if password.islower() or password.isupper():
        raise ValidationError("Password not made up of both upper and lower characters.",
                              code='password_not_upper_lower')


def check_image_type(image):
    """This function is used to check if the image both an image and a jpg file."""
    if not image.name.endswith(".jpg"):
        raise ValidationError("The photo must use the jpg format.", code='invalid_type')

def validate_image_size(fname):
    """ensure that the image size is smaller than 5mb"""
    size = os.path.getsize(fname)
    if size > 5242880:
        return "invalid"
    else:
        return "valid"

def validate_metadata(fname):
    """This function checks that gps and location metadata is included in the image."""
    with open(fname, 'rb') as image_file:
        my_image = Image(image_file)
    #raise ValidationError(my_image.list_all()) #used this line to see what metadata test images have
    if my_image.has_exif:
        #try to find metadata- however, if the metadata does not exist at all, there is an exception
        if my_image.gps_latitude_ref ==None or my_image.gps_latitude == None or my_image.gps_longitude_ref == None or my_image.gps_longitude == None:
            return "missing gps"

        elif my_image.datetime_original== None:
            return "missing datetime"

        else:
            return "valid"
    else:
        return "missing metadata"

