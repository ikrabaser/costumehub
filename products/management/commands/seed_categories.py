from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from products.models import Kategori


KATEGORI_AGACI = {
    "Kostümler": {
        "Çocuk Kostümleri": [
            "Süper Kahraman",
            "Prenses ve Masal",
            "Çizgi Film Karakterleri",
            "Hayvan Kostümleri",
            "Meslek Kostümleri",
            "Fantastik Kostümler",
            "Korku Kostümleri",
        ],
        "Yetişkin Kostümleri": [
            "Süper Kahraman",
            "Film ve Dizi Karakterleri",
            "Tarihî Kostümler",
            "Fantastik Kostümler",
            "Parti Kostümleri",
            "Meslek Kostümleri",
            "Korku Kostümleri",
        ],
        "Unisex Kostümler": [
            "Maskot Kostümleri",
            "Hayvan Kostümleri",
            "Fantastik Kostümler",
        ],
    },
}


class Command(BaseCommand):
    help = "CostumeHub kategori ağacını oluşturur veya günceller."

    @transaction.atomic
    def handle(self, *args, **options):
        for ana_sira, (ana_ad, alt_gruplar) in enumerate(
            KATEGORI_AGACI.items(),
            start=1,
        ):
            ana_kategori = self.kategori_olustur(
                ad=ana_ad,
                ust_kategori=None,
                sira=ana_sira,
            )

            for grup_sira, (grup_ad, yapraklar) in enumerate(
                alt_gruplar.items(),
                start=1,
            ):
                grup = self.kategori_olustur(
                    ad=grup_ad,
                    ust_kategori=ana_kategori,
                    sira=grup_sira,
                )

                for yaprak_sira, yaprak_ad in enumerate(
                    yapraklar,
                    start=1,
                ):
                    self.kategori_olustur(
                        ad=yaprak_ad,
                        ust_kategori=grup,
                        sira=yaprak_sira,
                    )

        self.stdout.write(
            self.style.SUCCESS(
                "Kategori ağacı başarıyla oluşturuldu/güncellendi."
            )
        )

    def kategori_olustur(
        self,
        ad,
        ust_kategori,
        sira,
    ):
        slug = slugify(ad)

        kategori, olusturuldu = Kategori.objects.get_or_create(
            ad=ad,
            ust_kategori=ust_kategori,
            defaults={
                "slug": slug,
                "aktif_mi": True,
                "sira": sira,
            },
        )

        degisti = False

        if kategori.slug != slug:
            kategori.slug = slug
            degisti = True

        if not kategori.aktif_mi:
            kategori.aktif_mi = True
            degisti = True

        if kategori.sira != sira:
            kategori.sira = sira
            degisti = True

        if degisti:
            kategori.save(
                update_fields=[
                    "slug",
                    "aktif_mi",
                    "sira",
                    "guncellenme_tarihi",
                ]
            )

        durum = "Oluşturuldu" if olusturuldu else "Mevcut"

        self.stdout.write(
            f"{durum}: {kategori.tam_yol}"
        )

        return kategori