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


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = (
        ('on_count', 'On count'),
        ('off_count', 'Off count'),
    )
    GENDER_CHOICE = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    COLOR_CHOICES = (
        ('blue', 'Blue'),
        ('red', 'Red'),
        ('orange', 'Orange'),
    )

    SIZE_CHOICES = (
        ('xxs', 'XXS'),
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
    )

    product_title = models.CharField(max_length=100, db_index=True)
    product_description = models.TextField(blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(
        upload_to="products/", blank=True)
    color = models.CharField(
        max_length=10, choices=COLOR_CHOICES)
    size = models.CharField(
        max_length=6, choices=SIZE_CHOICES)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='off_count')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(
        max_length=250, null=False, unique=True, db_index=True)

    class Meta:
        ordering = ('product_title',)
        index_together = (('id', 'slug'),)
        db_table = "ecommerce_product"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        app_label = "ecommerce_app"

    def __str__(self):
        return f'{self.product_title, self.product_price, self.status}'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/', blank=True)

    class Meta:
        db_table = "ecommerce_profile"
        verbose_name = "User profile"
        verbose_name_plural = "user profiles"

    def __str__(self):
        return f'Profile for user {self.user.username}'
