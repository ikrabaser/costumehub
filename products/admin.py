from django.contrib import admin

from .models import (
    Ilan,
    IlanOzellikDegeri,
    Kategori,
    KategoriOzellik,
    OzellikSecenegi,
)


class OzellikSecenegiInline(admin.TabularInline):
    model = OzellikSecenegi
    extra = 1

    fields = (
        "deger",
        "aktif_mi",
        "sira",
    )

    ordering = (
        "sira",
        "deger",
    )


class IlanOzellikDegeriInline(admin.TabularInline):
    model = IlanOzellikDegeri
    extra = 0

    fields = (
        "ozellik",
        "secenek",
        "metin_degeri",
    )

    autocomplete_fields = (
        "ozellik",
        "secenek",
    )


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


@admin.register(KategoriOzellik)
class KategoriOzellikAdmin(admin.ModelAdmin):
    list_display = (
        "ad",
        "kategori",
        "veri_tipi",
        "zorunlu_mu",
        "filtrelenebilir_mi",
        "aktif_mi",
        "sira",
    )

    list_filter = (
        "veri_tipi",
        "zorunlu_mu",
        "filtrelenebilir_mi",
        "aktif_mi",
        "kategori",
    )

    search_fields = (
        "ad",
        "kategori__ad",
        "kategori__slug",
    )

    autocomplete_fields = (
        "kategori",
    )

    ordering = (
        "kategori__ad",
        "sira",
        "ad",
    )

    inlines = (
        OzellikSecenegiInline,
    )

    fieldsets = (
        (
            "Özellik Bilgileri",
            {
                "fields": (
                    "kategori",
                    "ad",
                    "veri_tipi",
                )
            },
        ),
        (
            "Kullanım Ayarları",
            {
                "fields": (
                    "zorunlu_mu",
                    "filtrelenebilir_mi",
                    "aktif_mi",
                    "sira",
                )
            },
        ),
    )


@admin.register(OzellikSecenegi)
class OzellikSecenegiAdmin(admin.ModelAdmin):
    list_display = (
        "deger",
        "ozellik",
        "kategori_gosterimi",
        "aktif_mi",
        "sira",
    )

    list_filter = (
        "aktif_mi",
        "ozellik",
        "ozellik__kategori",
    )

    search_fields = (
        "deger",
        "ozellik__ad",
        "ozellik__kategori__ad",
    )

    autocomplete_fields = (
        "ozellik",
    )

    ordering = (
        "ozellik__kategori__ad",
        "ozellik__ad",
        "sira",
        "deger",
    )

    @admin.display(
        description="Kategori",
        ordering="ozellik__kategori__ad",
    )
    def kategori_gosterimi(self, nesne):
        return nesne.ozellik.kategori.tam_yol


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

    inlines = (
        IlanOzellikDegeriInline,
    )

    fieldsets = (
        (
            "Temel Bilgiler",
            {
                "fields": (
                    "ilan_sahibi",
                    "kategori",
                    "baslik",
                    "aciklama",
                    "fotograf",
                )
            },
        ),
        (
            "Ürün Bilgileri",
            {
                "fields": (
                    "beden",
                    "renk",
                    "sehir",
                )
            },
        ),
        (
            "Fiyat Bilgileri",
            {
                "fields": (
                    "gunluk_fiyat",
                    "depozito",
                )
            },
        ),
        (
            "Yayın ve Uygunluk",
            {
                "fields": (
                    "durum",
                    "mevcut_mu",
                )
            },
        ),
        (
            "Tarih Bilgileri",
            {
                "fields": (
                    "olusturulma_tarihi",
                    "guncellenme_tarihi",
                )
            },
        ),
    )


@admin.register(IlanOzellikDegeri)
class IlanOzellikDegeriAdmin(admin.ModelAdmin):
    list_display = (
        "ilan",
        "ozellik",
        "deger_gosterimi",
    )

    list_filter = (
        "ozellik",
        "ozellik__kategori",
    )

    search_fields = (
        "ilan__baslik",
        "ozellik__ad",
        "secenek__deger",
        "metin_degeri",
    )

    autocomplete_fields = (
        "ilan",
        "ozellik",
        "secenek",
    )

    @admin.display(
        description="Değer",
    )
    def deger_gosterimi(self, nesne):
        if nesne.secenek:
            return nesne.secenek.deger

        return nesne.metin_degeri