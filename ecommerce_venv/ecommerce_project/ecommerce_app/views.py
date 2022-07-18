
# Create your views here.
from locale import currency
from operator import countOf
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
from .models import Profile, NewUser,Product
from ecommerce_app.models import Cart,All_Orders,Order_Values
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
import mysql.connector
from datetime import date,datetime,timedelta

today=date.today()
now = datetime.now()
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="ecommerce"
    

)




mycursor=mydb.cursor()


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
        res=NewUser.objects.filter(email=email,password=password).count()
        
        if (res!=0):
            
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
    on_count = Product.objects.filter(status="on_count")
    off_count = Product.objects.filter(status="off_count")
    
    return render(request, 'mens.html', {'on_count': on_count,'off_count': off_count,})





def cart(request):
    product=Cart.objects.all()
    return render(request,'cart.html',{'cart':product})

num=[]
def add_to_cart(request):
    if request.method=="POST":
        id=request.POST['id']
        
    
        
        mydata = Product.objects.filter(id=id).values()
        
        values_by_id= {
            'mymembers': mydata,
        }
        b=values_by_id['mymembers'][0]
    
        
        Order_Number=1
        num.append(Order_Number)
        i=len(num)
        N_Order_Number= i + 1
        Cart(Order_Number=Order_Number,Order_Product=b['product_title'],Order_Product_Price=b['product_price'],Order_Product_Value="$",Order_Product_Image=b['product_image']).save()
        All_Orders(Order_Number=N_Order_Number,Order_Product_id=b['id'],Order_Product=b['product_title'],Order_Product_Price=b['product_price'],Order_Product_Value="$",Order_Product_Image=b['product_image']).save()
        
        on_count = Product.objects.filter(status="on_count")
        off_count = Product.objects.filter(status="off_count")
        number_of_items=Cart.objects.all().count()
        
        return render(request, 'mens.html', {'on_count': on_count,'off_count': off_count,"number_of_items":number_of_items})



def make_order(request):
    Cart.objects.all().delete()
    if request.method=="POST":
        price=request.POST['total_value']
        return render(request,'payment.html',{"price" : price})        
        


def finish_order(request):
    if request.method=="POST":
        Card_Number=request.POST['card']
        Name=request.POST['name']
        Expiration_Date=request.POST['expiration']
        Security_Code=request.POST['security']
        Price=request.POST['price']
        Date =today.strftime("%m/%d/%y")
        Time=now.strftime("%H:%M:%S")
        sql="select *from ecommerce_all_orders ORDER BY id DESC LIMIT 1;"

        mycursor.execute(sql)
        a=mycursor.fetchall()
        Order_Number=a[0][1]
        products=[]
        mydata = All_Orders.objects.filter(Order_Number=Order_Number).values()
        
        values_by_id= {
            'mymembers': mydata,
        }
        b=values_by_id['mymembers']
        for i in b:
            products.append(i['Order_Product_id'])
        products1=';'.join(products)
        
        Order_Values(Order_Number=Order_Number,Price=Price,Name=Name,Card_Number=Card_Number,Expiration_Date=Expiration_Date,Security_Code=Security_Code,Date=Date,Time=Time,Products=products1).save()

        return render(request,'payment.html',{"products":products1})





