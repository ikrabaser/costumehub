from django.urls import path

from . import views


app_name = "conversations"


urlpatterns = [
    path(
        "",
        views.sohbet_listesi,
        name="sohbet_listesi",
    ),
    path(
        "baslat/<int:ilan_id>/",
        views.sohbet_baslat,
        name="sohbet_baslat",
    ),
    path(
        "<int:sohbet_id>/",
        views.sohbet_detay,
        name="sohbet_detay",
    ),
]