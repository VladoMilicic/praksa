# Create your models here.
from django.conf import settings
from distutils.command.upload import upload
from tabnanny import verbose
from tkinter import Widget
from urllib.parse import MAX_CACHE_SIZE
from django.db import models
from django.db import connections
from django import forms
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField
from django import forms
from PIL import Image


class NewUser(models.Model):
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=50, null=False, blank=False)
    password2 = models.CharField(max_length=50, null=True, blank=False)

    class Meta:
        db_table = "ecommerce_newuser"
        verbose_name = "New user"
        verbose_name_plural = "New users"

    def __str__(self):
        return self.email


class Product(models.Model):
    STATUS_CHOICES = (
        ('on_count', 'On count'),
        ('off_count', 'Off count'),
    )

    Product_Title = models.TextField(max_length=100)
    Product_Price = models.IntegerField()
    Product_Image = models.ImageField(upload_to="products/", blank=True)
    Status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='off_count')
    Slug = models.SlugField(
        max_length=250, null=False)

    class Meta:
        db_table = "ecommerce_product"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f'{self.Product_Title, self.Product_Price, self.Status}'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    class Meta:
        db_table = "ecommerce_profile"
        verbose_name = "User profile"
        verbose_name_plural = "user profiles"

    def __str__(self):
        return f'Profile for user {self.user.username}'
