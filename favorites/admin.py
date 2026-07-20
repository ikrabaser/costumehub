from django.contrib import admin

from .models import Favori


@admin.register(Favori)
class FavoriAdmin(admin.ModelAdmin):
    list_display = (
        "kullanici",
        "ilan",
        "olusturulma_tarihi",
    )

    list_filter = (
        "olusturulma_tarihi",
    )

    search_fields = (
        "kullanici__username",
        "ilan__baslik",
    )