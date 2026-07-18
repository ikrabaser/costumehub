from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class KiralamaTalebi(models.Model):

    DURUM_SECENEKLERI = [
        ("BEKLIYOR", "Bekliyor"),
        ("KABUL_EDILDI", "Kabul Edildi"),
        ("REDDEDILDI", "Reddedildi"),
        ("IPTAL_EDILDI", "İptal Edildi"),
        ("TAMAMLANDI", "Tamamlandı"),
    ]

    ilan = models.ForeignKey(
        "products.Ilan",
        on_delete=models.CASCADE,
        related_name="kiralama_talepleri",
        verbose_name="İlan",
    )

    kiraci = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="kiralama_talepleri",
        verbose_name="Kiracı",
    )

    baslangic_tarihi = models.DateField(
        verbose_name="Başlangıç tarihi",
    )

    bitis_tarihi = models.DateField(
        verbose_name="Bitiş tarihi",
    )

    toplam_gun = models.PositiveIntegerField(
        verbose_name="Toplam gün",
    )

    toplam_tutar = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Toplam tutar",
    )

    durum = models.CharField(
        max_length=20,
        choices=DURUM_SECENEKLERI,
        default="BEKLIYOR",
        verbose_name="Talep durumu",
    )

    not_metni = models.TextField(
        blank=True,
        verbose_name="Kiracı notu",
    )

    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Oluşturulma tarihi",
    )

    guncellenme_tarihi = models.DateTimeField(
        auto_now=True,
        verbose_name="Güncellenme tarihi",
    )

    class Meta:
        verbose_name = "Kiralama talebi"
        verbose_name_plural = "Kiralama talepleri"
        ordering = ["-olusturulma_tarihi"]

    def __str__(self):
        return (
            f"{self.kiraci.username} - "
            f"{self.ilan.baslik} - "
            f"{self.get_durum_display()}"
        )

    def clean(self):
        if self.baslangic_tarihi and self.bitis_tarihi:

            if self.baslangic_tarihi < timezone.localdate():
                raise ValidationError(
                    {
                        "baslangic_tarihi": (
                            "Başlangıç tarihi geçmiş bir tarih olamaz."
                        )
                    }
                )

            if self.bitis_tarihi < self.baslangic_tarihi:
                raise ValidationError(
                    {
                        "bitis_tarihi": (
                            "Bitiş tarihi başlangıç tarihinden "
                            "önce olamaz."
                        )
                    }
                )

        if (
            self.kiraci_id
            and self.ilan_id
            and self.kiraci_id == self.ilan.ilan_sahibi_id
        ):
            raise ValidationError(
                "Kendi ilanınız için kiralama talebi oluşturamazsınız."
            )