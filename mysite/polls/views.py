"""This is to handle views, a function that takes a web request and returns a web response"""
import datetime
import operator
from pathlib import Path

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages

from .forms import ImagefieldForm
from .models import Image
from .forms import LoginForm, SignupForm
from .image_metadata import get_gps, get_time, get_distance
from .validate import validate_metadata, validate_image_size

def get_img_metadata(fname):
    """A function to return location and date taken from metadata"""
    return get_gps(fname), get_time(fname)

def is_photo_valid_for_challenge(gps, date_taken):
    # Checks to see if the photo was taken within 2km of campus
    #raise ValidationError(gps)
    if get_distance((50.7366, -3.5350), gps) <= 2:
        return True
    else:
        return False

def delete_Image_obj(obj):
    '''To fully delete an image object, delete the image, then the object'''
    obj.img.delete()
    obj.delete()

def not_authenticated():
    """If you are not authenticated (i.e. when trying to upload a photo) this displays"""
    return HttpResponse('You must be logged in to upload an image')

def invalid_metadata_popup(request,meta_status):
    """If the metadata is invalid, a will explain what is missing to the user"""
    if meta_status == "missing gps":
        messages.info(request, 'Photo must contain location data')
    elif meta_status == "missing datetime":
        messages.info(request, 'Photo must contain information about when it was taken')
    else:
        messages.info(request, 'Photo must contain information about when and where it was taken')

def invalid_image_size_popup(request, size_status):
    if size_status == "invalid":
        messages.info(request, 'Photo must be less than 5mb')

def upload_image(request):
    """This is used once the request has been made, process it.
    To test this page without logging in, comment out the next two lines"""
    context = {}

    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = ImagefieldForm(request.POST, request.FILES)
        # Sanitize inputs
        if form.is_valid():
            name = form.cleaned_data["name"]
            desc = form.cleaned_data["description"]
            img = form.cleaned_data["image"]
            # Create the table object
            obj = Image(
                title=name,
                description=desc,
                img=img,
                gps_coordinates=(0, 0),
                taken_date=datetime.datetime.now(),
                score=0
            )
            obj.user = request.user
            obj.save()

            #validate size of image, must be less than 5mb
            size_status = validate_image_size(Path('.' + obj.img.url))
            if size_status == "invalid":
                delete_Image_obj(obj)
                context['form'] = form
                invalid_image_size_popup(request,size_status) #message tells user of size error
                return render(request, "uploadfile.html", context) #refresh page
            #validate metadata
            meta_status = validate_metadata(Path('.' + obj.img.url))
            #add image metadata to database
            if meta_status == "valid":
                gps, date_taken = get_img_metadata(Path('.' + obj.img.url))
                obj.gps_coordinates = gps
                obj.taken_date = date_taken
            #if metadata is invalid then reject the submission
            else:
                delete_Image_obj(obj) #image is invalid so is deleted
                context['form'] = form
                invalid_metadata_popup(request,meta_status) #message tells user what metadata is missing
                return render(request, "uploadfile.html", context) #refresh page

            if is_photo_valid_for_challenge(gps, date_taken):
                return redirect('successful_upload')
            else:
                messages.info(request, 'Photo is either too far from challenge location or was taken outside the challenge timeframe')
                obj.img.delete()
                obj.delete()  # image is invalid, so deleted.

                context['form'] = form
                return render(request, "uploadfile.html", context)
    else:
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


def display_feed(request):
    """A view to display the photo feed to users"""
    # reverse order so latest submissions appear first- should be expanded later to make popular submissions stay near top
    all_images = Image.objects.all().order_by('-pk')
    # all_images = Image.objects.all()
    return render(request, 'feed.html', {'images': all_images})


def leaderboards(request):
    """A view to display the leaderboards"""
    all_images = Image.objects.all()
    score_d = {}
    for x in all_images:
        z = 0
        for y in list(score_d):
            if y == x.user:
                z = 1
                # if user is already in the dictionary, z = 1
        if z == 1:
            score_d[x.user] = score_d[x.user] + x.score
            # if z = 1, the new score is added to the existing score for the user.
        else:
            score_d[x.user] = x.score
    sorted_d = dict(sorted(score_d.items(), key=operator.itemgetter(1), reverse=True))
    # sorting the dictionary from highest value to lowest value

    return render(request, 'leaderboards.html', {'scores': sorted_d})
