from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("kayit/", views.kayit_ol, name="kayit"),
    path("giris/", views.giris_yap, name="giris"),
    path("cikis/", views.cikis_yap, name="cikis"),
]