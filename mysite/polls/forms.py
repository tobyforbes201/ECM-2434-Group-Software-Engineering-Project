"""This is used to handle all the forms."""
from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .validate import check_user_unique, validate_upper_lower, \
    validate_special, validate_number, check_image_type

from .models import Profile, Challenge


class ImagefieldForm(forms.Form):
    """The form used to upload a new image."""
    challenge = forms.ModelChoiceField(queryset=Challenge.objects.filter(active=True), initial=0)
    description = forms.CharField(widget=forms.Textarea(attrs={'style': "width:100%;"}),
                                  max_length=200)
    image = forms.ImageField(validators=[check_image_type])


class SignupForm(forms.Form):
    """The form used to sign up and create a new user. It requires a username and password,
    that are put through validators. Validate_password is django's default password validator
    and will check the password is 8 or longer, check if the password is simular to the username,
    check if the password is commonly used and check if it is fully numerical."""
    username = forms.CharField(validators=[check_user_unique], label="", max_length=30)
    password = forms.CharField(validators=[validate_password, validate_upper_lower,
                                           validate_special, validate_number],
                               label="", max_length=30, widget=forms.PasswordInput())


class LoginForm(forms.Form):
    """The form used to log in and authenticate this existing user,
    requiring a password and username"""
    username = forms.CharField(label="", max_length=30, required=True)
    password = forms.CharField(label="", max_length=30, widget=forms.PasswordInput(), required=True)

    def clean(self):
        """This method is used to check if the user exists and is an active user.
        This is done separately so that the error message can be displayed."""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("username or password is incorrect.")
        return self.cleaned_data

    def login(self):
        """This is used to authenticate the user and log in."""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class ProfileUpdateForm(forms.ModelForm):
    """Update user profile"""

    class Meta:
        """The meta class"""
        model = Profile
        fields = ['img']
