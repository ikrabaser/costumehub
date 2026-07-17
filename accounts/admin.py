from django.contrib import admin

from .models import Profil


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = (
        "kullanici",
        "telefon",
        "sehir",
        "olusturulma_tarihi",
    )

    search_fields = (
        "kullanici__username",
        "kullanici__email",
        "telefon",
        "sehir",
    )

    list_filter = (
        "sehir",
        "olusturulma_tarihi",
    )