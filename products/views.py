import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from decimal import Decimal, InvalidOperation

from rentals.models import KiralamaTalebi
from reviews.models import Degerlendirme
from favorites.models import Favori

from .forms import IlanFormu
from .models import (
    Ilan,
    IlanFotograf,
    IlanOzellikDegeri,
    Kategori,
    KategoriOzellik,
    OzellikSecenegi,
)


def home(request):
    return render(request, "products/home.html")
@require_GET
def kategori_alt_kategorileri(request, kategori_id):
    kategori = get_object_or_404(
        Kategori,
        id=kategori_id,
        aktif_mi=True,
    )

    alt_kategoriler = list(
        kategori.alt_kategoriler.filter(
            aktif_mi=True,
        )
        .order_by(
            "sira",
            "ad",
        )
        .values(
            "id",
            "ad",
            "slug",
        )
    )

    return JsonResponse(
        {
            "kategori": {
                "id": kategori.id,
                "ad": kategori.ad,
                "tam_yol": kategori.tam_yol,
            },
            "alt_kategoriler": alt_kategoriler,
            "alt_kategori_var_mi": bool(
                alt_kategoriler
            ),
        }
    )

@require_GET
def kategori_ozellikleri(request, kategori_id):
    kategori = get_object_or_404(
        Kategori,
        id=kategori_id,
        aktif_mi=True,
    )

    kategori_yolu = [
        *kategori.atalari_getir(),
        kategori,
    ]

    ozellikler = []

    for kategori_nesnesi in kategori_yolu:
        kategori_ozellikleri = (
            KategoriOzellik.objects.filter(
                kategori=kategori_nesnesi,
                aktif_mi=True,
            )
            .prefetch_related(
                "secenekler",
            )
            .order_by(
                "sira",
                "ad",
            )
        )

        for ozellik in kategori_ozellikleri:
            secenekler = []

            if ozellik.veri_tipi == "SECIM":
                secenekler = list(
                    ozellik.secenekler.filter(
                        aktif_mi=True,
                    )
                    .order_by(
                        "sira",
                        "deger",
                    )
                    .values(
                        "id",
                        "deger",
                    )
                )

            ozellikler.append(
                {
                    "id": ozellik.id,
                    "ad": ozellik.ad,
                    "veri_tipi": ozellik.veri_tipi,
                    "zorunlu_mu": ozellik.zorunlu_mu,
                    "filtrelenebilir_mi": (
                        ozellik.filtrelenebilir_mi
                    ),
                    "kategori": {
                        "id": kategori_nesnesi.id,
                        "ad": kategori_nesnesi.ad,
                    },
                    "secenekler": secenekler,
                }
            )

    return JsonResponse(
        {
            "kategori": {
                "id": kategori.id,
                "ad": kategori.ad,
                "tam_yol": kategori.tam_yol,
                "yaprak_kategori_mi": (
                    kategori.yaprak_kategori_mi
                ),
            },
            "ozellikler": ozellikler,
        }
    )


def kategori_ozelliklerini_getir(kategori):
    kategori_yolu = [
        *kategori.atalari_getir(),
        kategori,
    ]

    ozellikler = []

    for kategori_nesnesi in kategori_yolu:
        kategori_ozellikleri = (
            KategoriOzellik.objects.filter(
                kategori=kategori_nesnesi,
                aktif_mi=True,
            )
            .order_by(
                "sira",
                "ad",
            )
        )

        ozellikler.extend(
            kategori_ozellikleri
        )

    return ozellikler
@login_required
def ilan_olustur(request):
    secili_kategori = None

    if request.method == "POST":
        form = IlanFormu(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            kategori = form.cleaned_data["kategori"]
            fotograflar = form.cleaned_data.get(
                "fotograflar",
                [],
            )

            kategori_ozellikleri = (
                kategori_ozelliklerini_getir(
                    kategori
                )
            )

            kaydedilecek_degerler = []
            dinamik_alan_hatasi_var_mi = False

            for ozellik in kategori_ozellikleri:
                alan_adi = f"ozellik_{ozellik.id}"

                girilen_deger = request.POST.get(
                    alan_adi,
                    "",
                ).strip()

                if (
                    ozellik.zorunlu_mu
                    and not girilen_deger
                ):
                    form.add_error(
                        None,
                        (
                            f'"{ozellik.ad}" alanı '
                            "zorunludur."
                        ),
                    )

                    dinamik_alan_hatasi_var_mi = True
                    continue

                if not girilen_deger:
                    continue

                if ozellik.veri_tipi == "SECIM":
                    try:
                        secenek = (
                            OzellikSecenegi.objects.get(
                                id=girilen_deger,
                                ozellik=ozellik,
                                aktif_mi=True,
                            )
                        )

                        kaydedilecek_degerler.append(
                            {
                                "ozellik": ozellik,
                                "secenek": secenek,
                                "metin_degeri": "",
                            }
                        )

                    except (
                        OzellikSecenegi.DoesNotExist,
                        TypeError,
                        ValueError,
                    ):
                        form.add_error(
                            None,
                            (
                                f'"{ozellik.ad}" için '
                                "geçerli bir seçenek seçin."
                            ),
                        )

                        dinamik_alan_hatasi_var_mi = True

                elif ozellik.veri_tipi == "SAYI":
                    try:
                        sayisal_deger = Decimal(
                            girilen_deger.replace(
                                ",",
                                ".",
                            )
                        )

                        kaydedilecek_degerler.append(
                            {
                                "ozellik": ozellik,
                                "secenek": None,
                                "metin_degeri": str(
                                    sayisal_deger
                                ),
                            }
                        )

                    except InvalidOperation:
                        form.add_error(
                            None,
                            (
                                f'"{ozellik.ad}" alanına '
                                "geçerli bir sayı girin."
                            ),
                        )

                        dinamik_alan_hatasi_var_mi = True

                elif ozellik.veri_tipi == "EVET_HAYIR":
                    if girilen_deger not in [
                        "EVET",
                        "HAYIR",
                    ]:
                        form.add_error(
                            None,
                            (
                                f'"{ozellik.ad}" için '
                                "Evet veya Hayır seçin."
                            ),
                        )

                        dinamik_alan_hatasi_var_mi = True
                        continue

                    kaydedilecek_degerler.append(
                        {
                            "ozellik": ozellik,
                            "secenek": None,
                            "metin_degeri": girilen_deger,
                        }
                    )

                else:
                    kaydedilecek_degerler.append(
                        {
                            "ozellik": ozellik,
                            "secenek": None,
                            "metin_degeri": girilen_deger,
                        }
                    )

            if not dinamik_alan_hatasi_var_mi:
                with transaction.atomic():
                    ilan = form.save(
                        commit=False
                    )

                    ilan.ilan_sahibi = request.user
                    ilan.save()

                    for sira, fotograf in enumerate(
                        fotograflar
                    ):
                        ilan_fotografi = (
                            IlanFotograf.objects.create(
                                ilan=ilan,
                                fotograf=fotograf,
                                ana_fotograf_mi=(
                                    sira == 0
                                ),
                                sira=sira,
                            )
                        )

                        if sira == 0:
                            ilan.fotograf = (
                                ilan_fotografi.fotograf
                            )

                    if fotograflar:
                        ilan.save(
                            update_fields=[
                                "fotograf",
                            ]
                        )

                    for deger_bilgisi in (
                        kaydedilecek_degerler
                    ):
                        IlanOzellikDegeri.objects.create(
                            ilan=ilan,
                            ozellik=(
                                deger_bilgisi[
                                    "ozellik"
                                ]
                            ),
                            secenek=(
                                deger_bilgisi[
                                    "secenek"
                                ]
                            ),
                            metin_degeri=(
                                deger_bilgisi[
                                    "metin_degeri"
                                ]
                            ),
                        )

                messages.success(
                    request,
                    "İlanınız başarıyla oluşturuldu.",
                )

                return redirect(
                    "products:ilan_detay",
                    ilan_id=ilan.id,
                )

    else:
        baslangic_sehri = ""

        if hasattr(request.user, "profil"):
            baslangic_sehri = (
                request.user.profil.sehir
            )

        form = IlanFormu(
            initial={
                "sehir": baslangic_sehri,
            }
        )

    ana_kategoriler = list(
        Kategori.objects.filter(
            aktif_mi=True,
            ust_kategori__isnull=True,
        )
        .order_by(
            "sira",
            "ad",
        )
        .values(
            "id",
            "ad",
        )
    )

    secili_kategori_yolu = []

    secili_kategori_id = (
        request.POST.get("kategori")
        if request.method == "POST"
        else form.initial.get("kategori")
    )

    if secili_kategori_id:
        try:
            secili_kategori = Kategori.objects.get(
                id=secili_kategori_id,
                aktif_mi=True,
            )

            kategori_yolu = [
                *secili_kategori.atalari_getir(),
                secili_kategori,
            ]

            secili_kategori_yolu = [
                {
                    "id": kategori.id,
                    "ad": kategori.ad,
                    "ust_kategori_id": (
                        kategori.ust_kategori_id
                    ),
                }
                for kategori in kategori_yolu
            ]

        except (
            Kategori.DoesNotExist,
            TypeError,
            ValueError,
        ):
            secili_kategori_yolu = []

    context = {
        "form": form,
        "ana_kategoriler": ana_kategoriler,
        "secili_kategori_yolu": (
            secili_kategori_yolu
        ),
    }

    return render(
        request,
        "products/ilan_olustur.html",
        context,
    )

def kategori_ve_alt_kategori_idleri(kategori):
    kategori_idleri = [kategori.id]

    alt_kategoriler = kategori.alt_kategoriler.filter(
        aktif_mi=True,
    )

    for alt_kategori in alt_kategoriler:
        kategori_idleri.extend(
            kategori_ve_alt_kategori_idleri(
                alt_kategori
            )
        )
    return kategori_idleri


def ilan_listesi(request):
    ilanlar = (
        Ilan.objects.filter(
            durum="YAYINDA",
            mevcut_mu=True,
        )
        .select_related(
            "kategori",
            "ilan_sahibi",
        )
        .order_by("-olusturulma_tarihi")
    )

    arama = request.GET.get(
        "arama",
        "",
    ).strip()

    kategori = request.GET.get(
        "kategori",
        "",
    ).strip()

    beden = request.GET.get(
        "beden",
        "",
    ).strip()

    sehir = request.GET.get(
        "sehir",
        "",
    ).strip()

    maksimum_fiyat = request.GET.get(
        "maksimum_fiyat",
        "",
    ).strip()


    if arama:
        ilanlar = ilanlar.filter(
            Q(baslik__icontains=arama)
            | Q(aciklama__icontains=arama)
            | Q(renk__icontains=arama)
        )


    secili_kategori = None
    secili_kategori_yolu = []

    if kategori:
        try:
            secili_kategori = Kategori.objects.get(
                id=kategori,
                aktif_mi=True,
            )

            kategori_idleri = (
                kategori_ve_alt_kategori_idleri(
                    secili_kategori
                )
            )

            ilanlar = ilanlar.filter(
                kategori_id__in=kategori_idleri,
            )

            kategori_yolu = [
                *secili_kategori.atalari_getir(),
                secili_kategori,
            ]

            secili_kategori_yolu = [
                {
                    "id": kategori_nesnesi.id,
                    "ad": kategori_nesnesi.ad,
                    "ust_kategori_id": (
                        kategori_nesnesi.ust_kategori_id
                    ),
                }
                for kategori_nesnesi in kategori_yolu
            ]

        except (
            Kategori.DoesNotExist,
            TypeError,
            ValueError,
        ):
            kategori = ""
            secili_kategori = None
            secili_kategori_yolu = []


    if beden:
        ilanlar = ilanlar.filter(
            beden=beden,
        )


    if sehir:
        ilanlar = ilanlar.filter(
            sehir__icontains=sehir,
        )


    if maksimum_fiyat:
        try:
            maksimum_fiyat_degeri = float(
                maksimum_fiyat
            )

            if maksimum_fiyat_degeri >= 0:
                ilanlar = ilanlar.filter(
                    gunluk_fiyat__lte=(
                        maksimum_fiyat_degeri
                    ),
                )

        except ValueError:
            pass


    ana_kategoriler = list(
        Kategori.objects.filter(
            aktif_mi=True,
            ust_kategori__isnull=True,
        )
        .order_by(
            "sira",
            "ad",
        )
        .values(
            "id",
            "ad",
        )
    )


    context = {

        "ilanlar": ilanlar,
        "ana_kategoriler": ana_kategoriler,
        "secili_kategori_yolu": secili_kategori_yolu,
        "beden_secenekleri": Ilan.BEDEN_SECENEKLERI,
        "arama": arama,
        "secili_kategori": kategori,
        "secili_beden": beden,
        "sehir": sehir,
        "maksimum_fiyat": maksimum_fiyat,

    }

    return render(
        request,
        "products/ilan_listesi.html",
        context,
    )


def ilan_detay(request, ilan_id):
    ilan = get_object_or_404(
        Ilan.objects.select_related(
            "kategori",
            "ilan_sahibi",
            "ilan_sahibi__profil",
        ),
        id=ilan_id,
        durum="YAYINDA",
    )
    favoride_mi = False

    if request.user.is_authenticated:
        favoride_mi = Favori.objects.filter(
             kullanici=request.user,
               ilan=ilan,
                 ).exists()
       

    bugun = timezone.localdate()

    dolu_tarih_araliklari = list(
        KiralamaTalebi.objects.filter(
            ilan=ilan,
            durum__in=[
                "KABUL_EDILDI",
                "TESLIM_EDILDI",
                "IADE_EDILDI",
                "TAMAMLANDI",
            ],
            bitis_tarihi__gte=bugun,
        )
        .order_by("baslangic_tarihi")
        .values(
            "baslangic_tarihi",
            "bitis_tarihi",
        )
    )

    dolu_tarihler_json = json.dumps(
        [
            {
                "baslangic": tarih[
                    "baslangic_tarihi"
                ].isoformat(),
                "bitis": tarih[
                    "bitis_tarihi"
                ].isoformat(),
            }
            for tarih in dolu_tarih_araliklari
        ]
    )

    degerlendirmeler = (
        Degerlendirme.objects.filter(
            kiralama_talebi__ilan=ilan,
        )
        .select_related(
            "degerlendiren",
            "kiralama_talebi",
        )
        .order_by("-olusturulma_tarihi")
    )

    degerlendirme_istatistikleri = (
        degerlendirmeler.aggregate(
            ortalama_puan=Avg("puan"),
        )
    )

    ortalama_puan = (
        degerlendirme_istatistikleri[
            "ortalama_puan"
        ]
    )

    degerlendirme_sayisi = (
        degerlendirmeler.count()
    )
    
    ozellik_degerleri = (
        IlanOzellikDegeri.objects
        .filter(ilan=ilan)
        .select_related(
            "ozellik",
            "secenek",
        )
        .order_by(
            "ozellik__sira",
            "ozellik__ad",
        )
    )

    kategori_yolu = [
        *ilan.kategori.atalari_getir(),
        ilan.kategori,
    ]

    context = {
        "ilan": ilan,
        "dolu_tarih_araliklari": dolu_tarih_araliklari,
        "dolu_tarihler_json": dolu_tarihler_json,
        "degerlendirmeler": degerlendirmeler,
        "ortalama_puan": ortalama_puan,
        "degerlendirme_sayisi": degerlendirme_sayisi,
        "favoride_mi": favoride_mi,
        "ozellik_degerleri": ozellik_degerleri,
        "kategori_yolu": kategori_yolu,
    }
    return render(
        request,
        "products/ilan_detay.html",
        context,
    )