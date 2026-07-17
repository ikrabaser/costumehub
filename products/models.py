from django.conf import settings
from django.db import models


class Kategori(models.Model):
    ad = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Kategori adı",
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
    )

    aktif_mi = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?",
    )

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ["ad"]

    def __str__(self):
        return self.ad


class Ilan(models.Model):
    BEDEN_SECENEKLERI = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
        ("STANDART", "Standart"),
    ]

    DURUM_SECENEKLERI = [
        ("TASLAK", "Taslak"),
        ("YAYINDA", "Yayında"),
        ("PASIF", "Pasif"),
    ]

    ilan_sahibi = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ilanlar",
        verbose_name="İlan sahibi",
    )

    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.PROTECT,
        related_name="ilanlar",
        verbose_name="Kategori",
    )

    baslik = models.CharField(
        max_length=150,
        verbose_name="İlan başlığı",
    )

    aciklama = models.TextField(
        max_length=2000,
        verbose_name="Açıklama",
    )

    beden = models.CharField(
        max_length=20,
        choices=BEDEN_SECENEKLERI,
        verbose_name="Beden",
    )

    renk = models.CharField(
        max_length=50,
        verbose_name="Renk",
    )

    gunluk_fiyat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Günlük kiralama ücreti",
    )

    depozito = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Depozito",
    )

    sehir = models.CharField(
        max_length=50,
        verbose_name="Şehir",
    )

    durum = models.CharField(
        max_length=20,
        choices=DURUM_SECENEKLERI,
        default="YAYINDA",
        verbose_name="İlan durumu",
    )

    mevcut_mu = models.BooleanField(
        default=True,
        verbose_name="Kiralamaya uygun mu?",
    )

    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True,
    )

    guncellenme_tarihi = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "İlan"
        verbose_name_plural = "İlanlar"
        ordering = ["-olusturulma_tarihi"]

    def __str__(self):
        return self.baslik