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
