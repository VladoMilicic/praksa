from django.contrib import admin
from .models import NewUser, Product, Profile
# Register your models here.
admin.site.register(NewUser)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('Status', 'Product_Title',
                    'Product_Price', 'Product_Image', 'Slug')
    list_filter = ('Status', 'Product_Title', 'Product_Price')
    search_fields = ('Product_Title', 'Product_Price')
    prepopulated_fields = {'Slug': ('Product_Title', )}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
