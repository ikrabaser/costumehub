from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.home, name="home"),
    path("ilan-ver/", views.ilan_olustur, name="ilan_olustur"),
]