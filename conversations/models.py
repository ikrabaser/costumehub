from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from products.models import Ilan


class Sohbet(models.Model):
    ilan = models.ForeignKey(
        Ilan,
        on_delete=models.CASCADE,
        related_name="sohbetler",
    )

    kiraci = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="kiraci_sohbetleri",
    )

    ilan_sahibi = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ilan_sahibi_sohbetleri",
    )

    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True,
    )

    guncellenme_tarihi = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-guncellenme_tarihi",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "ilan",
                    "kiraci",
                ],
                name="benzersiz_ilan_kiraci_sohbeti",
            ),
        ]

        verbose_name = "Sohbet"
        verbose_name_plural = "Sohbetler"

    def clean(self):
        super().clean()

        if self.kiraci_id == self.ilan_sahibi_id:
            raise ValidationError(
                "Kiracı ve ilan sahibi aynı kullanıcı olamaz."
            )

        if (
            self.ilan_id
            and self.ilan_sahibi_id
            and self.ilan.ilan_sahibi_id != self.ilan_sahibi_id
        ):
            raise ValidationError(
                "Sohbetteki ilan sahibi, ilanın sahibiyle eşleşmiyor."
            )

    def __str__(self):
        return (
            f"{self.ilan.baslik} - "
            f"{self.kiraci.username}"
        )


class Mesaj(models.Model):
    sohbet = models.ForeignKey(
        Sohbet,
        on_delete=models.CASCADE,
        related_name="mesajlar",
    )

    gonderen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gonderilen_mesajlar",
    )

    icerik = models.TextField(
        max_length=1000,
    )

    okundu_mu = models.BooleanField(
        default=False,
    )

    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "olusturulma_tarihi",
        ]

        verbose_name = "Mesaj"
        verbose_name_plural = "Mesajlar"

    def clean(self):
        super().clean()

        if not self.sohbet_id or not self.gonderen_id:
            return

        izinli_kullanicilar = [
            self.sohbet.kiraci_id,
            self.sohbet.ilan_sahibi_id,
        ]

        if self.gonderen_id not in izinli_kullanicilar:
            raise ValidationError(
                "Bu kullanıcı bu sohbete mesaj gönderemez."
            )

    def __str__(self):
        return (
            f"{self.gonderen.username}: "
            f"{self.icerik[:40]}"
        )