from django.contrib import admin

from .models import Mesaj, Sohbet


class MesajInline(admin.TabularInline):
    model = Mesaj
    extra = 0
    readonly_fields = [
        "olusturulma_tarihi",
    ]


@admin.register(Sohbet)
class SohbetAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "ilan",
        "kiraci",
        "ilan_sahibi",
        "guncellenme_tarihi",
    ]

    list_filter = [
        "olusturulma_tarihi",
        "guncellenme_tarihi",
    ]

    search_fields = [
        "ilan__baslik",
        "kiraci__username",
        "ilan_sahibi__username",
    ]

    readonly_fields = [
        "olusturulma_tarihi",
        "guncellenme_tarihi",
    ]

    inlines = [
        MesajInline,
    ]


@admin.register(Mesaj)
class MesajAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "sohbet",
        "gonderen",
        "okundu_mu",
        "olusturulma_tarihi",
    ]

    list_filter = [
        "okundu_mu",
        "olusturulma_tarihi",
    ]

    search_fields = [
        "icerik",
        "gonderen__username",
        "sohbet__ilan__baslik",
    ]

    readonly_fields = [
        "olusturulma_tarihi",
    ]