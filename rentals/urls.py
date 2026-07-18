from django.urls import path

from . import views


app_name = "rentals"

urlpatterns = [
    path(
        "ilan/<int:ilan_id>/talep-olustur/",
        views.kiralama_talebi_olustur,
        name="kiralama_talebi_olustur",
    ),
]