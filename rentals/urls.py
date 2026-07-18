from django.urls import path

from . import views

app_name = "rentals"

urlpatterns = [
    path(
        "ilan/<int:ilan_id>/talep-olustur/",
        views.kiralama_talebi_olustur,
        name="kiralama_talebi_olustur",
    ),

    path(
        "gelen-talepler/",
        views.gelen_kiralama_talepleri,
        name="gelen_kiralama_talepleri",
    ),

    path(
        "talep/<int:talep_id>/kabul-et/",
        views.kiralama_talebi_kabul_et,
        name="kiralama_talebi_kabul_et",
    ),

    path(
        "talep/<int:talep_id>/reddet/",
        views.kiralama_talebi_reddet,
        name="kiralama_talebi_reddet",
    ),
]