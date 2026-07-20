from django.conf import settings
from django.db import models

from products.models import Ilan


class Favori(models.Model):
    kullanici = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorileri",
    )

    ilan = models.ForeignKey(
        Ilan,
        on_delete=models.CASCADE,
        related_name="favoriye_ekleyenler",
    )

    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "kullanici",
                    "ilan",
                ],
                name="benzersiz_kullanici_ilan_favorisi",
            )
        ]

        ordering = [
            "-olusturulma_tarihi",
        ]

        verbose_name = "Favori"
        verbose_name_plural = "Favoriler"

    def __str__(self):
        return (
            f"{self.kullanici.username} - "
            f"{self.ilan.baslik}"
        )