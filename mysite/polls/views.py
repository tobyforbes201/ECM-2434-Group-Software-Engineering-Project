"""This is to handle views, a function that takes a web request and returns a web response"""
import datetime

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

from .forms import ImagefieldForm
from .models import Image
from .forms import LoginForm, SignupForm


def get_img_metadata(img):
    """A placeholder function to return location and date taken from metadata"""
    return '1.001 1.002', datetime.datetime.now()


def not_authenticated():
    """If you are not authenticated (i.e. when trying to upload a photo) this displays"""
    return HttpResponse('You must be logged in to upload an image')


def upload_image(request):
    """This is used once the request has been made, process it.
    To test this page without logging in, comment out the next two lines"""
    context = {}

    if not request.user.is_authenticated:
        return redirect('not_authenticated')
    if request.method == "POST":
        form = ImagefieldForm(request.POST, request.FILES)
        # Sanitize inputs
        if form.is_valid():
            name = form.cleaned_data["name"]
            desc = form.cleaned_data["description"]
            img = form.cleaned_data["image"]
            gps, date_taken = get_img_metadata(img)
            # Create the table object
            obj = Image(
                title=name,
                description=desc,
                img=img,
                gps_coordinates=gps,
                taken_date=date_taken,
                score=0
            )
            obj.user = request.user
            obj.save()
            return redirect('successful_upload')
    # display the image upload form
    form = ImagefieldForm()
    context['form'] = form
    return render(request, "uploadfile.html", context)


def successful_upload(request):
    """Displayed on a successful upload of an image."""
    return render(request, "imagesuccess.html")


def signup(request):
    """A view for registration of a new user. If the form passes the validators,
    a new user will be created. By default, the password is both hashed and salted."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Sanitise the inputs
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username,
                                     password=password)
            return HttpResponseRedirect('/polls/login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    """A view for logging in an already registered user."""
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login()
        if user:
            auth_login(request, user)
            return HttpResponseRedirect('/polls/')
    return render(request, 'login.html', {'form': form})


def home(request):
    """A view for the homepage, used to access other views."""
    return render(request, 'home.html')


def logout(request):
    """A view to log out the user"""
    auth_logout(request)
    return HttpResponseRedirect('/polls/')
