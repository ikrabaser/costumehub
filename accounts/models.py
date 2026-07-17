from django.contrib.auth.models import User
from django.db import models


class Profil(models.Model):
    kullanici = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profil",
    )

    telefon = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="Telefon",
    )

    sehir = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Şehir",
    )

    biyografi = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Biyografi",
    )

    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True,
    )

    guncellenme_tarihi = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profiller"

    def __str__(self):
        return f"{self.kullanici.username} profili"