from atexit import register
from django.contrib import admin
from .models import NewUser, Product, Profile, Category
# Register your models here.
admin.site.register(NewUser)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('status', 'sex', 'product_title',
                    'product_price', 'size', 'color', 'product_image', 'created', 'updated', 'slug')
    list_display_links = ['color', ]
    list_filter = ('sex', 'status', 'product_title', 'product_price')
    list_editable = ['sex', 'product_price', 'status', 'size']
    search_fields = ('product_title', 'product_price')
    prepopulated_fields = {'slug': ('product_title', )}


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
