from django.contrib import admin

from .models import Ilan, Kategori


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = (
        "ad",
        "slug",
        "aktif_mi",
    )

    search_fields = (
        "ad",
        "slug",
    )

    list_filter = (
        "aktif_mi",
    )

    prepopulated_fields = {
        "slug": ("ad",),
    }


@admin.register(Ilan)
class IlanAdmin(admin.ModelAdmin):
    list_display = (
        "baslik",
        "ilan_sahibi",
        "kategori",
        "beden",
        "gunluk_fiyat",
        "sehir",
        "durum",
        "mevcut_mu",
        "olusturulma_tarihi",
    )

    search_fields = (
        "baslik",
        "aciklama",
        "ilan_sahibi__username",
        "kategori__ad",
        "sehir",
    )

    list_filter = (
        "kategori",
        "beden",
        "durum",
        "mevcut_mu",
        "sehir",
        "olusturulma_tarihi",
    )

    list_select_related = (
        "ilan_sahibi",
        "kategori",
    )

    readonly_fields = (
        "olusturulma_tarihi",
        "guncellenme_tarihi",
    )