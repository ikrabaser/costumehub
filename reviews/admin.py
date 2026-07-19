from django.contrib import admin

from .models import Degerlendirme


@admin.register(Degerlendirme)
class DegerlendirmeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "kiralama_talebi",
        "degerlendiren",
        "degerlendirilen",
        "puan",
        "olusturulma_tarihi",
    ]

    list_filter = [
        "puan",
        "olusturulma_tarihi",
    ]

    search_fields = [
        "yorum",
        "degerlendiren__username",
        "degerlendirilen__username",
        "kiralama_talebi__ilan__baslik",
    ]

    readonly_fields = [
        "olusturulma_tarihi",
        "guncellenme_tarihi",
    ]

    ordering = [
        "-olusturulma_tarihi",
    ]