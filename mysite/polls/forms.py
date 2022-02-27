"""This is used to handle all the forms."""
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.password_validation import validate_password

from .validate import check_user_unique, validate_upper_lower, validate_special, validate_number


class SignupForm(forms.Form):
    """The form used to sign up and create a new user. It requires a username and password,
    that are put through validators. Validate_password is django's default password validator
    and will check the password is 8 or longer, check if the password is simular to the username,
    check if the password is commonly used and check if it is fully numerical."""
    username = forms.CharField(validators=[check_user_unique], label="", max_length=30)
    password = forms.CharField(validators=[validate_password, validate_upper_lower,
                                           validate_special, validate_number],
                               label="", max_length=30)


class LoginForm(forms.Form):
    """The form used to log in and authenticate this existing user,
    requiring a password and username"""
    username = forms.CharField(label=mark_safe('<br><br>Username'), max_length=30)
    password = forms.CharField(label=mark_safe('<br><br>Password'), max_length=30)
