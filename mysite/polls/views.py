"""This is to handle views, a function that takes a web request and returns a web response"""
import datetime
import operator
from pathlib import Path

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Image, Vote, Badge, Challenge
from .forms import LoginForm, SignupForm, ImagefieldForm, ProfileUpdateForm
from .image_metadata import get_gps, get_time, get_distance
from .validate import validate_metadata, validate_image_size


def get_img_metadata(fname):
    """A function to return location and date taken from metadata."""
    return get_gps(fname), get_time(fname)


def is_photo_valid_for_challenge(gps, date_taken):
    """Checks to see if the photo was taken within 2km of campus
    raise ValidationError(gps)."""
    if get_distance((50.7366, -3.5350), gps) <= 2:
        # After this, the date should also be validated.
        return True
    return False


def delete_image_obj(obj):
    """To fully delete an image object, delete the image, then the object"""
    obj.img.delete()
    obj.delete()


def get_user_score_and_images(user):
    """This gets a users score, total number of photos and a list of the images"""
    score = 0
    total_photos = 0
    user_images = Image.objects.filter(user=user)
    for image in user_images:
        score += image.score
        total_photos += 1
    return score, total_photos, user_images


def invalid_metadata_popup(request, meta_status):
    """If the metadata is invalid, a popup will explain what is missing to the user"""
    if meta_status == "missing gps":
        messages.info(request, 'Photo must contain location data')
    elif meta_status == "missing datetime":
        messages.info(request, 'Photo must contain information about when it was taken')
    else:
        messages.info(request, 'Photo must contain information about when and where it was taken')


def invalid_image_size_popup(request, size_status):
    """If the size status is below 5mb , a popup will display the error."""
    if size_status == "invalid":
        messages.info(request, 'Photo must be less than 5mb')


def check_badge(request):
    """This is used to check if a new badge should be added for the current user"""
    current_user = request.user
    score, total_images, _ = get_user_score_and_images(current_user)
    if score >= 10 and Badge.objects.filter(user=current_user,
                                            name="Ten Total Score").first() is None:
        badge = Badge(
            user=current_user,
            name="Ten Total Score",
            description="A post got voted on, earning you ten points!",
            badge_image="badges/10scorebadge.png",
        )
        badge.save()
    if score >= 100 and Badge.objects.filter(user=current_user,
                                             name="Hundred Total Score").first() is None:
        badge = Badge(
            user=current_user,
            name="Hundred Total Score",
            description="Ten of your posts got voted on",
            badge_image="badges/100scorebadge.png",
        )
        badge.save()
    if score >= 1000 and Badge.objects.filter(user=current_user,
                                              name="Thousand Total Score").first() is None:
        badge = Badge(
            user=current_user,
            name="Thousand Total Score",
            description="A hundred of your posts got voted on, well done!",
            badge_image="badges/1000scorebadge.png",
        )
        badge.save()
    if total_images >= 1 and Badge.objects.filter(user=current_user,
                                                  name="One Total Image").first() is None:
        badge = Badge(
            user=current_user,
            name="One Total Image",
            description="Uploaded a photo to the feed",
            badge_image="badges/1totalbadge.png",
        )
        badge.save()
    if total_images >= 10 and Badge.objects.filter(user=current_user,
                                                   name="Ten Total Images").first() is None:
        badge = Badge(
            user=current_user,
            name="Ten Total Images",
            description="Uploaded ten photos.",
            badge_image="badges/10totalbadge.png",
        )
        badge.save()
    if total_images >= 100 and Badge.objects.filter(user=current_user,
                                                    name="Hundred Total Images").first() is None:
        badge = Badge(
            user=current_user,
            name="Hundred Total Images",
            description="Uploaded hundred photos!",
            badge_image="badges/100totalbadge.png",
        )
        badge.save()



def upload_image(request):
    """This is used once the request has been made, process it.
    To test this page without logging in, comment out the next two lines"""
    context = {}

    if not request.user.is_authenticated:
        return redirect('login')
    for challenge in Challenge.objects.all():
        Challenge.is_active(challenge)

    if request.method == "POST":

        form = ImagefieldForm(request.POST, request.FILES)
        # Sanitize inputs

        if form.is_valid():
            challenge = form.cleaned_data["challenge"]
            name = form.cleaned_data["name"]
            desc = form.cleaned_data["description"]
            img = form.cleaned_data["image"]
            # Create the table object
            obj = Image(
                challenge=challenge,
                title=name,
                description=desc,
                img=img,
                gps_coordinates=(0, 0),
                taken_date=datetime.datetime.now(),
                score=0
            )
            obj.user = request.user
            obj.save()

            # validate size of image, must be less than 5mb
            size_status = validate_image_size(Path('.' + obj.img.url))
            if size_status == "invalid":
                delete_image_obj(obj)
                context['form'] = form
                invalid_image_size_popup(request, size_status)  # message tells user of size error
                return render(request, "uploadfile.html", context)  # refresh page
            # validate metadata
            meta_status = validate_metadata(Path('.' + obj.img.url))
            # add image metadata to database
            if meta_status == "valid":
                gps, date_taken = get_img_metadata(Path('.' + obj.img.url))
                obj.gps_coordinates = gps
                obj.taken_date = datetime.datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
            # if metadata is invalid then reject the submission
            else:
                delete_image_obj(obj)  # image is invalid so is deleted
                context['form'] = form
                invalid_metadata_popup(request, meta_status)
                # message tells user what metadata is missing
                return render(request, "uploadfile.html", context)  # refresh page

            if is_photo_valid_for_challenge(gps, date_taken):
                obj.save()
                return redirect('successful_upload')
            messages.info(request, 'Photo is either too far from challenge'
                                   ' location or was taken outside the challenge timeframe')
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
    # reverse order so the latest submissions appear first-
    # should be expanded later to make popular submissions stay near top
    all_images = Image.objects.all().order_by('-pk')
    return render(request, 'feed.html', {'images': all_images})


def leaderboards(request):
    """A view to display the leaderboards"""
    all_images = Image.objects.all()
    score_d = {}
    for image in all_images:
        user_in_directory = False
        for user in list(score_d):
            if user == image.user:
                user_in_directory = True
        if user_in_directory:
            score_d[image.user] = score_d[image.user] + image.score
            # User in directory, the new score is added to the existing score for the user.
        else:
            score_d[image.user] = image.score
    sorted_d = dict(sorted(score_d.items(), key=operator.itemgetter(1), reverse=True))
    # Sorting the dictionary from the highest value to the lowest value

    return render(request, 'leaderboards.html', {'scores': sorted_d})


def profile(request):
    """where a user can manage their account, including account and post deletion
    and changing profile pictures"""
    if not request.user.is_authenticated:
        return redirect('login')


    check_badge(request)
    badges = Badge.objects.filter(user=request.user)
    score, total_photos, user_images = get_user_score_and_images(request.user)

    user_images = Image.objects.filter(user=request.user)
    score = 0
    total_photos = 0
    for image in user_images:
        score += image.score
        total_photos += 1

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')  # Redirect back to profile page

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form,
        'images': user_images,
        'score': score,
        'total_photos': total_photos,
        'badges': badges,
    }

    return render(request, 'profile.html', context)


def view_profile(request, username=None):
    """view a user's profile"""
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    score, total_photos, user_images = get_user_score_and_images(user)

    context = {
        'images': user_images,
        'score': score,
        'total_photos': total_photos,
        'view_user': user
    }

    return render(request, 'viewprofile.html', context)


def delete_photo(request, photo_id=None):
    """delete a user's photo by replacing it with a placeholder"""
    photo_to_delete = Image.objects.get(id=photo_id)
    photo_to_delete.img = str(Path('./picture/error.jpg'))
    photo_to_delete.title = "This photo was removed"
    photo_to_delete.description = "User deleted the photo"
    photo_to_delete.save()

    return redirect('profile')


def delete_account(request, username=None):
    """delete a user's account"""
    user_to_delete = User.objects.get(username=username)
    user_images = Image.objects.filter(user=user_to_delete)
    for img in user_images:
        img.delete()
    user_to_delete.delete()

    return HttpResponseRedirect('/polls/')


def vote(request, photo_id):
    """user votes for a photo"""
    if request.method == "POST":
        # make sure user can't like the photo more than once.
        user = User.objects.get(username=request.user.username)
        # find whatever photo is associated with vote
        photo = Image.objects.get(id=photo_id)

        new_vote = Vote(user=user, image=photo)
        new_vote.already_voted = True

        photo.score += 10
        # adds user to photoS
        photo.user_votes.add(user)
        photo.save()
        new_vote.save()
        return redirect('feed')
    return redirect('feed')


def unvote(request, photo_id):
    """user revokes their vote for a photo"""
    if request.method == "POST":
        # make sure user can't like the photo more than once.
        user = User.objects.get(username=request.user.username)
        # find whatever post is associated with vote
        photo = Image.objects.get(id=photo_id)

        revoke_vote = Vote.objects.get(user=user, image=photo)
        # delete the vote
        revoke_vote.delete()

        photo.score -= 10
        # remove user from photo
        photo.user_votes.remove(user)
        photo.save()

        return redirect('feed')
    return redirect('feed')
