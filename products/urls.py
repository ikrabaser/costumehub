from django.urls import path

from . import views


app_name = "products"


urlpatterns = [
    path(
        "",
        views.home,
        name="home",
    ),
    path(
        "ilanlar/",
        views.ilan_listesi,
        name="ilan_listesi",
    ),
    path(
        "ilan-ver/",
        views.ilan_olustur,
        name="ilan_olustur",
    ),
    path(
        "ilanlar/<int:ilan_id>/",
        views.ilan_detay,
        name="ilan_detay",
    ),
    path(
        "kategoriler/<int:kategori_id>/alt-kategoriler/",
        views.kategori_alt_kategorileri,
        name="kategori_alt_kategorileri",
    ),
    path(
    "kategoriler/<int:kategori_id>/ozellikler/",
    views.kategori_ozellikleri,
    name="kategori_ozellikleri",
    ),
    
]