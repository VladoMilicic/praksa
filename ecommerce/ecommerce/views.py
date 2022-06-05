import re
from typing import NoReturn
from django.db.models.query import EmptyQuerySet
from django.http import request,HttpResponse
from django.http.response import HttpResponseRedirect
import mysql.connector
from django.http import HttpResponse
from django.shortcuts import redirect, render


def HomePage(request):
    return render(request,'homepage.html')

def localStores(request):
    return render(request,'Local-stores.html')

def productView(request):
    return render(request,'product-view.html')   

def sign_in(request):
    return render (request,'sign-in.html')
