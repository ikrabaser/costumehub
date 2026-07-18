from django.contrib import admin

from .models import KiralamaTalebi


@admin.register(KiralamaTalebi)
class KiralamaTalebiAdmin(admin.ModelAdmin):

    list_display = (
        "ilan",
        "kiraci",
        "baslangic_tarihi",
        "bitis_tarihi",
        "toplam_tutar",
        "durum",
    )

    list_filter = (
        "durum",
        "baslangic_tarihi",
    )

    search_fields = (
        "ilan__baslik",
        "kiraci__username",
    )

    readonly_fields = (
        "olusturulma_tarihi",
        "guncellenme_tarihi",
    )