"""This is used for functions that validate values in forms."""

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


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
