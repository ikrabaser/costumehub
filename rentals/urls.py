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
        "benim-taleplerim/",
        views.benim_kiralama_taleplerim,
        name="benim_kiralama_taleplerim",
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

    path(
        "talep/<int:talep_id>/teslim-et/",
        views.kiralama_talebi_teslim_et,
        name="kiralama_talebi_teslim_et",
    ),

    path(
        "talep/<int:talep_id>/iade-al/",
        views.kiralama_talebi_iade_al,
        name="kiralama_talebi_iade_al",
    ),

    path(
        "talep/<int:talep_id>/tamamla/",
        views.kiralama_talebi_tamamla,
        name="kiralama_talebi_tamamla",
    ),
]