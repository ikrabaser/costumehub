from django.urls import path

from . import views

app_name = "favorites"

urlpatterns = [
    path(
        "degistir/<int:ilan_id>/",
        views.favori_degistir,
        name="favori_degistir",
    ),
    path(
    "",
    views.favorilerim,
    name="favorilerim",
    ),
]