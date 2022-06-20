
# Create your views here.
import re
from typing import NoReturn
from django.db.models.query import EmptyQuerySet
from django.http import request, HttpResponse
from django.http.response import HttpResponseRedirect
import mysql.connector
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Profile, NewUser
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm


def base(request):
    return render(request, 'base.html')


def homePage(request):
    return render(request, 'homepage.html')


def header(request):
    return render(request, 'header.html')


def footer(request):
    return render(request, 'footer.html', )


def localStores(request):
    return render(request, 'local-stores.html')


def productView(request):
    return render(request, 'product-view.html')


def lookbook(request):
    return render(request, 'lookbook.html')


def signIn(request):  # rename to register
    if request.method == "POST":
        signin_form = UserRegistrationForm(request.POST)
        if signin_form.is_valid():
            signin_form.save()
            return HttpResponseRedirect('sign-in')
    else:
        signin_form = UserRegistrationForm()
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponse("Proradio materi")
        else:
            # Return an 'invalid login' error message.
            return HttpResponse("Ne radi")
    else:
        login_form = LoginForm()

    return render(request, 'sign-in.html', {"signin_form": signin_form, "login_form": login_form})


@login_required
def dashboard(request):
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register_done(request):
    return render(request, 'account/register_done.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['Password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'log-in.html',
                  {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def mens(request):
    ctx = Product.objects.all()
    return render(request, 'mens.html', {'products': ctx})
