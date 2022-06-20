from django import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.base, name="base"),
    path('homepage', views.homePage, name="homepage"),
    path('local-stores', views.localStores, name="local-stores"),
    path('sign-in', views.signIn, name="sign-in"),
    path('lookbook', views.lookbook, name="lookbook"),
    path('product-view', views.productView, name="product-view"),
    path('mens', views.mens, name="mens"),
    path('header', views.header, name="header"),
    path('footer', views.footer, name="footer"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
