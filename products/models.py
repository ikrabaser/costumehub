from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Kategori(models.Model):
    ad = models.CharField(
        max_length=100,
        verbose_name="Kategori adı",
    )

    slug = models.SlugField(
        max_length=120,
        verbose_name="URL adı",
    )

    ust_kategori = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="alt_kategoriler",
        verbose_name="Üst kategori",
    )

    aktif_mi = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?",
    )

    sira = models.PositiveIntegerField(
        default=0,
        verbose_name="Sıra",
        help_text="Kategorilerin gösterim sırasını belirler.",
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
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

        ordering = [
            "sira",
            "ad",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "ad",
                ],
                condition=Q(ust_kategori__isnull=True),
                name="benzersiz_ana_kategori_adi",
            ),
            models.UniqueConstraint(
                fields=[
                    "slug",
                ],
                condition=Q(ust_kategori__isnull=True),
                name="benzersiz_ana_kategori_slug",
            ),
            models.UniqueConstraint(
                fields=[
                    "ust_kategori",
                    "ad",
                ],
                condition=Q(ust_kategori__isnull=False),
                name="benzersiz_alt_kategori_adi",
            ),
            models.UniqueConstraint(
                fields=[
                    "ust_kategori",
                    "slug",
                ],
                condition=Q(ust_kategori__isnull=False),
                name="benzersiz_alt_kategori_slug",
            ),
        ]

    def __str__(self):
        return self.tam_yol

    def clean(self):
        super().clean()

        if self.ust_kategori is None:
            return

        if self.pk and self.ust_kategori_id == self.pk:
            raise ValidationError(
                {
                    "ust_kategori": (
                        "Bir kategori kendi üst kategorisi olamaz."
                    )
                }
            )

        kontrol_edilen_kategori = self.ust_kategori
        ziyaret_edilen_kategoriler = set()

        while kontrol_edilen_kategori is not None:
            if kontrol_edilen_kategori.pk in ziyaret_edilen_kategoriler:
                raise ValidationError(
                    {
                        "ust_kategori": (
                            "Kategori ağacında geçersiz bir döngü bulundu."
                        )
                    }
                )

            ziyaret_edilen_kategoriler.add(
                kontrol_edilen_kategori.pk
            )

            if (
                self.pk
                and kontrol_edilen_kategori.pk == self.pk
            ):
                raise ValidationError(
                    {
                        "ust_kategori": (
                            "Bu seçim kategori ağacında döngü "
                            "oluşturur."
                        )
                    }
                )

            kontrol_edilen_kategori = (
                kontrol_edilen_kategori.ust_kategori
            )

    @property
    def tam_yol(self):
        kategori_adlari = [
            self.ad,
        ]

        ust_kategori = self.ust_kategori
        ziyaret_edilenler = set()

        while ust_kategori is not None:
            if ust_kategori.pk in ziyaret_edilenler:
                break

            ziyaret_edilenler.add(
                ust_kategori.pk
            )

            kategori_adlari.append(
                ust_kategori.ad
            )

            ust_kategori = (
                ust_kategori.ust_kategori
            )

        kategori_adlari.reverse()

        return " > ".join(
            kategori_adlari
        )

    @property
    def seviye(self):
        seviye = 0
        ust_kategori = self.ust_kategori
        ziyaret_edilenler = set()

        while ust_kategori is not None:
            if ust_kategori.pk in ziyaret_edilenler:
                break

            ziyaret_edilenler.add(
                ust_kategori.pk
            )

            seviye += 1

            ust_kategori = (
                ust_kategori.ust_kategori
            )

        return seviye

    @property
    def yaprak_kategori_mi(self):
        return not self.alt_kategoriler.filter(
            aktif_mi=True
        ).exists()

    def atalari_getir(self):
        atalar = []
        ust_kategori = self.ust_kategori
        ziyaret_edilenler = set()

        while ust_kategori is not None:
            if ust_kategori.pk in ziyaret_edilenler:
                break

            ziyaret_edilenler.add(
                ust_kategori.pk
            )

            atalar.append(
                ust_kategori
            )

            ust_kategori = (
                ust_kategori.ust_kategori
            )

        atalar.reverse()

        return atalar


class KategoriOzellik(models.Model):
    VERI_TIPI_SECENEKLERI = [
        ("SECIM", "Seçim kutusu"),
        ("METIN", "Metin"),
        ("SAYI", "Sayı"),
        ("EVET_HAYIR", "Evet / Hayır"),
    ]

    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.CASCADE,
        related_name="ozellikler",
        verbose_name="Kategori",
    )

    ad = models.CharField(
        max_length=100,
        verbose_name="Özellik adı",
    )

    veri_tipi = models.CharField(
        max_length=20,
        choices=VERI_TIPI_SECENEKLERI,
        default="SECIM",
        verbose_name="Veri tipi",
    )

    zorunlu_mu = models.BooleanField(
        default=False,
        verbose_name="Zorunlu mu?",
    )

    filtrelenebilir_mi = models.BooleanField(
        default=True,
        verbose_name="Filtrelenebilir mi?",
        help_text=(
            "Bu özellik ilan filtreleme alanında "
            "gösterilsin mi?"
        ),
    )

    aktif_mi = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?",
    )

    sira = models.PositiveIntegerField(
        default=0,
        verbose_name="Sıra",
    )

    olusturulma_tarihi = models.DateTimeField(
        auto_now_add=True,
    )

    guncellenme_tarihi = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Kategori özelliği"
        verbose_name_plural = "Kategori özellikleri"

        ordering = [
            "sira",
            "ad",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "kategori",
                    "ad",
                ],
                name="benzersiz_kategori_ozelligi",
            ),
        ]

    def __str__(self):
        return (
            f"{self.kategori.tam_yol} > "
            f"{self.ad}"
        )


class OzellikSecenegi(models.Model):
    ozellik = models.ForeignKey(
        KategoriOzellik,
        on_delete=models.CASCADE,
        related_name="secenekler",
        verbose_name="Özellik",
    )

    deger = models.CharField(
        max_length=100,
        verbose_name="Seçenek değeri",
    )

    aktif_mi = models.BooleanField(
        default=True,
        verbose_name="Aktif mi?",
    )

    sira = models.PositiveIntegerField(
        default=0,
        verbose_name="Sıra",
    )

    class Meta:
        verbose_name = "Özellik seçeneği"
        verbose_name_plural = "Özellik seçenekleri"

        ordering = [
            "sira",
            "deger",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "ozellik",
                    "deger",
                ],
                name="benzersiz_ozellik_secenegi",
            ),
        ]

    def __str__(self):
        return (
            f"{self.ozellik.ad}: "
            f"{self.deger}"
        )


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

    fotograf = models.ImageField(
        upload_to="ilanlar/",
        blank=True,
        null=True,
        verbose_name="İlan fotoğrafı",
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

        ordering = [
            "-olusturulma_tarihi",
        ]

    def __str__(self):
        return self.baslik


class IlanOzellikDegeri(models.Model):
    ilan = models.ForeignKey(
        Ilan,
        on_delete=models.CASCADE,
        related_name="ozellik_degerleri",
        verbose_name="İlan",
    )

    ozellik = models.ForeignKey(
        KategoriOzellik,
        on_delete=models.PROTECT,
        related_name="ilan_degerleri",
        verbose_name="Özellik",
    )

    secenek = models.ForeignKey(
        OzellikSecenegi,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ilan_degerleri",
        verbose_name="Seçilen seçenek",
    )

    metin_degeri = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Girilen değer",
    )

    class Meta:
        verbose_name = "İlan özellik değeri"
        verbose_name_plural = "İlan özellik değerleri"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "ilan",
                    "ozellik",
                ],
                name="ilanda_benzersiz_ozellik_degeri",
            ),
        ]

    def clean(self):
        super().clean()

        if (
            self.secenek
            and self.secenek.ozellik_id
            != self.ozellik_id
        ):
            raise ValidationError(
                {
                    "secenek": (
                        "Seçilen değer bu özelliğe "
                        "ait değildir."
                    )
                }
            )

        if self.ozellik.veri_tipi == "SECIM":
            if self.secenek is None:
                raise ValidationError(
                    {
                        "secenek": (
                            "Bu özellik için bir seçenek "
                            "seçilmelidir."
                        )
                    }
                )

            if self.metin_degeri:
                raise ValidationError(
                    {
                        "metin_degeri": (
                            "Seçim tipi özelliklerde ayrıca "
                            "metin girilemez."
                        )
                    }
                )

        elif self.secenek is not None:
            raise ValidationError(
                {
                    "secenek": (
                        "Bu özellik seçim kutusu türünde "
                        "değildir."
                    )
                }
            )

    def __str__(self):
        if self.secenek:
            deger = self.secenek.deger
        else:
            deger = self.metin_degeri

        return (
            f"{self.ilan.baslik} - "
            f"{self.ozellik.ad}: {deger}"
        )