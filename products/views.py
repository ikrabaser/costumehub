import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from rentals.models import KiralamaTalebi
from reviews.models import Degerlendirme
from favorites.models import Favori

from .forms import IlanFormu
from .models import Ilan, Kategori


def home(request):
    return render(request, "products/home.html")


@login_required
def ilan_olustur(request):
    if request.method == "POST":
        form = IlanFormu(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            ilan = form.save(commit=False)
            ilan.ilan_sahibi = request.user
            ilan.save()

            messages.success(
                request,
                "İlanınız başarıyla oluşturuldu.",
            )

            return redirect("products:home")

    else:
        form = IlanFormu(
            initial={
                "sehir": request.user.profil.sehir,
            }
        )

    return render(
        request,
        "products/ilan_olustur.html",
        {
            "form": form,
        },
    )


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

    arama = request.GET.get("arama", "").strip()
    kategori = request.GET.get("kategori", "").strip()
    beden = request.GET.get("beden", "").strip()
    sehir = request.GET.get("sehir", "").strip()
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

    if kategori:
        ilanlar = ilanlar.filter(
            kategori_id=kategori,
        )

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
                    gunluk_fiyat__lte=maksimum_fiyat_degeri,
                )

        except ValueError:
            pass

    kategoriler = Kategori.objects.filter(
        aktif_mi=True,
    ).order_by("ad")

    context = {
        "ilanlar": ilanlar,
        "kategoriler": kategoriler,
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
    

    context = {
        "ilan": ilan,
        "dolu_tarih_araliklari": dolu_tarih_araliklari,
        "dolu_tarihler_json": dolu_tarihler_json,
        "degerlendirmeler": degerlendirmeler,
        "ortalama_puan": ortalama_puan,
        "degerlendirme_sayisi": degerlendirme_sayisi,
        "favoride_mi": favoride_mi,
    }

    return render(
        request,
        "products/ilan_detay.html",
        context,
    )