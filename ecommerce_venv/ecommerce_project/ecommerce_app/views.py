
# Create your views here.
from cgitb import html
from itertools import count
import re
from typing import NoReturn
from xml.dom import NotFoundErr
from django.db.models.query import EmptyQuerySet
from django.http import Http404, request, HttpResponse
from django.http.response import HttpResponseRedirect
import mysql.connector
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import pkg_resources
from .models import Product
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Profile, NewUser, Category, Product
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm


def base(request):
    return render(request, 'base.html')


def homePage(request):
    return render(request, 'homepage.html')


def header(request):
    if signIn(request) == True:
        return request('homepage')
    else:
        return HttpResponse("You must be loged in")
    return render(request, 'header.html')


def footer(request):
    return render(request, 'footer.html', )


def localStores(request):
    return render(request, 'local-stores.html')


def productView(request):
    slug = None
    if request.method == 'GET':
        slug = Product.objects.filter(slug="dzempr")
        if slug is not None:
            product = Product.objects.filter(slug="dzemper").get()
            return redirect('product-view/<slug:product>')
        else:
            return html("<h>product not found!</h>")
    return render(request, 'product-view.hvaljatml/<slug:slug>/', {'product': product})


def get_apsolute_url(self):  # absolute url for slugfield//testirati da li
    return f'/products/{self.slug}/'


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
        res = NewUser.objects.filter(email=email, password=password).count()

        if (res != 0):

            # Redirect to a success page.
            return HttpResponseRedirect('product-view')
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


def mens(request, category_slug=None):
    category = None
    male_products = Product.objects.all().filter(sex='male')
    available = Product.objects.filter(status='on_count')
    if category_slug and available:
        category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'mens.html', {'male_products': male_products})
