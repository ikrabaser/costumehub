from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from rentals.models import KiralamaTalebi


class Degerlendirme(models.Model):
    kiralama_talebi = models.OneToOneField(
        KiralamaTalebi,
        on_delete=models.CASCADE,
        related_name="degerlendirme",
    )

    degerlendiren = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="yaptigi_degerlendirmeler",
    )

    degerlendirilen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="aldigi_degerlendirmeler",
    )

    puan = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    yorum = models.TextField(
        max_length=1000,
    )

    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True,
    )

    guncellenme_tarihi = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-olusturulma_tarihi",
        ]

        verbose_name = "Değerlendirme"
        verbose_name_plural = "Değerlendirmeler"

    def clean(self):
        super().clean()

        if not self.kiralama_talebi_id:
            return

        if self.kiralama_talebi.durum != "TAMAMLANDI":
            raise ValidationError(
                "Yalnızca tamamlanmış kiralamalar değerlendirilebilir."
            )

        if self.degerlendiren_id != self.kiralama_talebi.kiraci_id:
            raise ValidationError(
                "Bu kiralamayı yalnızca kiracı değerlendirebilir."
            )

        if (
            self.degerlendirilen_id
            != self.kiralama_talebi.ilan.ilan_sahibi_id
        ):
            raise ValidationError(
                "Değerlendirilen kullanıcı ilan sahibi olmalıdır."
            )

        if self.degerlendiren_id == self.degerlendirilen_id:
            raise ValidationError(
                "Kullanıcı kendisini değerlendiremez."
            )

    def __str__(self):
        return (
            f"{self.degerlendiren.username} → "
            f"{self.degerlendirilen.username} "
            f"({self.puan}/5)"
        )