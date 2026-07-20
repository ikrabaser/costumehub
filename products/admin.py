from django.contrib import admin

from .models import Ilan, Kategori


@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = (
        "kategori_yolu",
        "ust_kategori",
        "seviye_gosterimi",
        "aktif_mi",
        "sira",
    )

    list_filter = (
        "aktif_mi",
        "ust_kategori",
    )

    search_fields = (
        "ad",
        "slug",
    )

    ordering = (
        "ust_kategori__id",
        "sira",
        "ad",
    )

    prepopulated_fields = {
        "slug": (
            "ad",
        )
    }

    autocomplete_fields = (
        "ust_kategori",
    )

    fieldsets = (
        (
            "Kategori Bilgileri",
            {
                "fields": (
                    "ad",
                    "slug",
                    "ust_kategori",
                )
            },
        ),
        (
            "Yayın Ayarları",
            {
                "fields": (
                    "aktif_mi",
                    "sira",
                )
            },
        ),
    )

    @admin.display(
        description="Kategori yolu",
        ordering="ad",
    )
    def kategori_yolu(self, nesne):
        return nesne.tam_yol

    @admin.display(
        description="Seviye",
    )
    def seviye_gosterimi(self, nesne):
        return nesne.seviye


@admin.register(Ilan)
class IlanAdmin(admin.ModelAdmin):
    list_display = (
        "baslik",
        "ilan_sahibi",
        "kategori",
        "gunluk_fiyat",
        "sehir",
        "durum",
        "mevcut_mu",
        "olusturulma_tarihi",
    )

    list_filter = (
        "durum",
        "mevcut_mu",
        "kategori",
        "sehir",
        "olusturulma_tarihi",
    )

    search_fields = (
        "baslik",
        "aciklama",
        "ilan_sahibi__username",
        "kategori__ad",
    )

    autocomplete_fields = (
        "kategori",
        "ilan_sahibi",
    )

    ordering = (
        "-olusturulma_tarihi",
    )

    readonly_fields = (
        "olusturulma_tarihi",
        "guncellenme_tarihi",
    )