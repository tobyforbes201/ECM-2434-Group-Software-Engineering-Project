"""This is to handle views, a function that takes a web request and returns a web response"""
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User

from .forms import LoginForm, SignupForm


def signup(request):
    """A view for registration of a new user. If the form passes the validators,
    a new user will be created. By default, the password is both hashed and salted."""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username,
                                     password=password)
            return HttpResponseRedirect('/polls/login/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    """A view for logging in an already registered user."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect('/polls/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home(request):
    """A view for the homepage, used to access other views."""
    return render(request, 'home.html')


def logout(request):
    """A view to log out the user"""
    auth_logout(request)
    return HttpResponseRedirect('/polls/')
