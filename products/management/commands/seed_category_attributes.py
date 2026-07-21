from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import (
    Kategori,
    KategoriOzellik,
    OzellikSecenegi,
)


KATEGORI_OZELLIKLERI = [
    {
        "kategori_yolu": [
            "Kostümler",
            "Çocuk Kostümleri",
            "Süper Kahraman",
        ],
        "ozellikler": [
            {
                "ad": "Yaş Grubu",
                "veri_tipi": "SECIM",
                "zorunlu_mu": True,
                "filtrelenebilir_mi": True,
                "secenekler": [
                    "3-5 Yaş",
                    "6-8 Yaş",
                    "9-12 Yaş",
                    "13-15 Yaş",
                ],
            },
            {
                "ad": "Cinsiyet",
                "veri_tipi": "SECIM",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": True,
                "secenekler": [
                    "Kız",
                    "Erkek",
                    "Unisex",
                ],
            },
            {
                "ad": "Marka",
                "veri_tipi": "METIN",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": True,
            },
            {
                "ad": "Kullanım Durumu",
                "veri_tipi": "SECIM",
                "zorunlu_mu": True,
                "filtrelenebilir_mi": True,
                "secenekler": [
                    "Sıfır",
                    "Bir Kez Kullanıldı",
                    "Az Kullanıldı",
                    "İyi Durumda",
                    "Onarım Gördü",
                ],
            },
        ],
    },
    {
        "kategori_yolu": [
            "Kostümler",
            "Yetişkin Kostümleri",
            "Süper Kahraman",
        ],
        "ozellikler": [
            {
                "ad": "Cinsiyet",
                "veri_tipi": "SECIM",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": True,
                "secenekler": [
                    "Kadın",
                    "Erkek",
                    "Unisex",
                ],
            },
            {
                "ad": "Marka",
                "veri_tipi": "METIN",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": True,
            },
            {
                "ad": "Kullanım Durumu",
                "veri_tipi": "SECIM",
                "zorunlu_mu": True,
                "filtrelenebilir_mi": True,
                "secenekler": [
                    "Sıfır",
                    "Bir Kez Kullanıldı",
                    "Az Kullanıldı",
                    "İyi Durumda",
                    "Onarım Gördü",
                ],
            },
            {
                "ad": "Parça Sayısı",
                "veri_tipi": "SAYI",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": False,
            },
        ],
    },
    {
        "kategori_yolu": [
            "Özel Gün Kıyafetleri",
            "Düğün",
            "Gelinlik",
        ],
        "ozellikler": [
            {
                "ad": "Kesim",
                "veri_tipi": "SECIM",
                "zorunlu_mu": True,
                "filtrelenebilir_mi": True,
                "secenekler": [
                    "A Kesim",
                    "Balık",
                    "Prenses",
                    "Helen",
                    "Düz Kesim",
                    "Mini",
                ],
            },
            {
                "ad": "Kumaş",
                "veri_tipi": "SECIM",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": True,
                "secenekler": [
                    "Saten",
                    "Dantel",
                    "Tül",
                    "Şifon",
                    "Organze",
                ],
            },
            {
                "ad": "Duvak Dahil mi?",
                "veri_tipi": "EVET_HAYIR",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": True,
            },
            {
                "ad": "Tesettür mü?",
                "veri_tipi": "EVET_HAYIR",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": True,
            },
            {
                "ad": "Kuru Temizleme Yapıldı mı?",
                "veri_tipi": "EVET_HAYIR",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": False,
            },
        ],
    },
    {
        "kategori_yolu": [
            "Cosplay",
            "Çizgi Roman",
            "Marvel",
        ],
        "ozellikler": [
            {
                "ad": "Karakter Adı",
                "veri_tipi": "METIN",
                "zorunlu_mu": True,
                "filtrelenebilir_mi": True,
            },
            {
                "ad": "El Yapımı mı?",
                "veri_tipi": "EVET_HAYIR",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": True,
            },
            {
                "ad": "Parça Sayısı",
                "veri_tipi": "SAYI",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": False,
            },
            {
                "ad": "Kullanım Durumu",
                "veri_tipi": "SECIM",
                "zorunlu_mu": True,
                "filtrelenebilir_mi": True,
                "secenekler": [
                    "Sıfır",
                    "Bir Kez Kullanıldı",
                    "Az Kullanıldı",
                    "İyi Durumda",
                    "Onarım Gördü",
                ],
            },
        ],
    },
    {
        "kategori_yolu": [
            "Aksesuarlar",
            "Baş Aksesuarları",
            "Maske",
        ],
        "ozellikler": [
            {
                "ad": "Malzeme",
                "veri_tipi": "SECIM",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": True,
                "secenekler": [
                    "Plastik",
                    "Kumaş",
                    "Lateks",
                    "Metal",
                    "Deri",
                ],
            },
            {
                "ad": "Ayarlanabilir mi?",
                "veri_tipi": "EVET_HAYIR",
                "zorunlu_mu": False,
                "filtrelenebilir_mi": True,
            },
            {
                "ad": "Kullanım Durumu",
                "veri_tipi": "SECIM",
                "zorunlu_mu": True,
                "filtrelenebilir_mi": True,
                "secenekler": [
                    "Sıfır",
                    "Bir Kez Kullanıldı",
                    "Az Kullanıldı",
                    "İyi Durumda",
                    "Onarım Gördü",
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Kategori özelliklerini ve seçeneklerini oluşturur."

    @transaction.atomic
    def handle(self, *args, **options):
        for kategori_verisi in KATEGORI_OZELLIKLERI:
            kategori = self.kategori_bul(
                kategori_verisi["kategori_yolu"]
            )

            for sira, ozellik_verisi in enumerate(
                kategori_verisi["ozellikler"],
                start=1,
            ):
                ozellik = self.ozellik_olustur(
                    kategori=kategori,
                    ozellik_verisi=ozellik_verisi,
                    sira=sira,
                )

                for secenek_sira, deger in enumerate(
                    ozellik_verisi.get("secenekler", []),
                    start=1,
                ):
                    self.secenek_olustur(
                        ozellik=ozellik,
                        deger=deger,
                        sira=secenek_sira,
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Kategori özellikleri başarıyla oluşturuldu/güncellendi."
            )
        )

    def kategori_bul(self, kategori_yolu):
        ust_kategori = None

        for kategori_adi in kategori_yolu:
            ust_kategori = Kategori.objects.get(
                ad=kategori_adi,
                ust_kategori=ust_kategori,
            )

        return ust_kategori

    def ozellik_olustur(
        self,
        kategori,
        ozellik_verisi,
        sira,
    ):
        ozellik, olusturuldu = (
            KategoriOzellik.objects.get_or_create(
                kategori=kategori,
                ad=ozellik_verisi["ad"],
                defaults={
                    "veri_tipi": ozellik_verisi["veri_tipi"],
                    "zorunlu_mu": ozellik_verisi["zorunlu_mu"],
                    "filtrelenebilir_mi": (
                        ozellik_verisi["filtrelenebilir_mi"]
                    ),
                    "aktif_mi": True,
                    "sira": sira,
                },
            )
        )

        degisti = False

        alanlar = {
            "veri_tipi": ozellik_verisi["veri_tipi"],
            "zorunlu_mu": ozellik_verisi["zorunlu_mu"],
            "filtrelenebilir_mi": (
                ozellik_verisi["filtrelenebilir_mi"]
            ),
            "aktif_mi": True,
            "sira": sira,
        }

        for alan_adi, yeni_deger in alanlar.items():
            if getattr(ozellik, alan_adi) != yeni_deger:
                setattr(ozellik, alan_adi, yeni_deger)
                degisti = True

        if degisti:
            ozellik.save()

        durum = "Oluşturuldu" if olusturuldu else "Mevcut"

        self.stdout.write(
            f"{durum}: {ozellik}"
        )

        return ozellik

    def secenek_olustur(
        self,
        ozellik,
        deger,
        sira,
    ):
        secenek, olusturuldu = (
            OzellikSecenegi.objects.get_or_create(
                ozellik=ozellik,
                deger=deger,
                defaults={
                    "aktif_mi": True,
                    "sira": sira,
                },
            )
        )

        degisti = False

        if not secenek.aktif_mi:
            secenek.aktif_mi = True
            degisti = True

        if secenek.sira != sira:
            secenek.sira = sira
            degisti = True

        if degisti:
            secenek.save()

        durum = "Oluşturuldu" if olusturuldu else "Mevcut"

        self.stdout.write(
            f"  {durum} seçenek: {secenek}"
        )