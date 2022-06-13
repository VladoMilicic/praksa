from django.db import models
from django.db import connections
from django import forms
from django.db.models.base import Model
from django.db.models.fields import CharField, IntegerField



class NewUser(models.Model):
    Username=models.CharField(max_length=150)
    Email=models.CharField(max_length=150)
    Pwd=models.CharField(max_length=150)
    Age=models.IntegerField()
    class Meta:
        db_table="ecommerce_newuser"


class Product(models.Model):
    Product_Title=models.TextField(max_length=100)
    Product_Price=models.IntegerField(max_length=10)
    Product_Image=models.CharField(max_length=50)
    class Meta:
        db_table="ecommerce_product"