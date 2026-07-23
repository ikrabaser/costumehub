from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import GirisFormu, KayitFormu, ProfilFormu
from products.models import Ilan
from rentals.models import KiralamaTalebi
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone


def kayit(request):
    if request.user.is_authenticated:
        return redirect("accounts:panel")

    if request.method == "POST":
        form = KayitFormu(request.POST)

        if form.is_valid():
            kullanici = form.save()
            login(request, kullanici)

            messages.success(
                request,
                "Hesabınız başarıyla oluşturuldu. CostumeHub'a hoş geldiniz!",
            )

            return redirect("accounts:panel")
    else:
        form = KayitFormu()

    return render(
        request,
        "accounts/kayit.html",
        {
            "form": form,
        },
    )


def giris(request):
    if request.user.is_authenticated:
        return redirect("accounts:panel")

    if request.method == "POST":
        form = GirisFormu(request, data=request.POST)

        if form.is_valid():
            kullanici = form.get_user()
            login(request, kullanici)

            messages.success(
                request,
                f"Hoş geldiniz, {kullanici.username}!",
            )

            return redirect("accounts:panel")
    else:
        form = GirisFormu()

    return render(
        request,
        "accounts/giris.html",
        {
            "form": form,
        },
    )


def cikis(request):
    if request.method == "POST":
        logout(request)

        messages.success(
            request,
            "Hesabınızdan başarıyla çıkış yaptınız.",
        )

    return redirect("products:home")

@login_required
def profil(request):
    profil_nesnesi = request.user.profil

    if request.method == "POST":
        form = ProfilFormu(
            request.POST,
            instance=profil_nesnesi,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Profil bilgileriniz başarıyla güncellendi.",
            )

            return redirect("accounts:profil")
    else:
        form = ProfilFormu(instance=profil_nesnesi)

    return render(
        request,
        "accounts/profil.html",
        {
            "profil": profil_nesnesi,
            "form": form,
        },
    )
@login_required
def panel(request):
    kullanici_ilanlari = Ilan.objects.filter(
        ilan_sahibi=request.user
    )
    son_ilanlar = kullanici_ilanlari.select_related(
        "kategori"
    )[:3]

    son_gelen_talepler = (
        KiralamaTalebi.objects.filter(
            ilan__ilan_sahibi=request.user
        )
        .select_related(
            "ilan",
            "kiraci",
        )[:3]
    )
    bugun = timezone.localdate()
    baslangic_tarihi = bugun - timedelta(days=6)

    gunluk_ilan_sorgusu = (
        kullanici_ilanlari.filter(
            olusturulma_tarihi__date__range=(
                baslangic_tarihi,
                bugun,
            )
        )
        .annotate(
            gun=TruncDate("olusturulma_tarihi")
        )
        .values("gun")
        .annotate(
            ilan_sayisi=Count("id")
        )
        .order_by("gun")
    )

    gunluk_ilan_sayilari = {
        kayit["gun"]: kayit["ilan_sayisi"]
        for kayit in gunluk_ilan_sorgusu
    }

    gun_adlari = [
        "Pzt",
        "Sal",
        "Çar",
        "Per",
        "Cum",
        "Cmt",
        "Paz",
    ]

    ilan_grafik_etiketleri = []
    ilan_grafik_verileri = []

    for gun_farki in range(7):
        tarih = baslangic_tarihi + timedelta(
            days=gun_farki
        )

        ilan_grafik_etiketleri.append(
            gun_adlari[tarih.weekday()]
        )

        ilan_grafik_verileri.append(
            gunluk_ilan_sayilari.get(tarih, 0)
        )
            # Kullanıcının ilanlarına gelen taleplerin durum dağılımı
    talep_durum_adlari = {
        "BEKLIYOR": "Bekliyor",
        "KABUL_EDILDI": "Kabul Edildi",
        "TESLIM_EDILDI": "Teslim Edildi",
        "IADE_EDILDI": "İade Edildi",
        "TAMAMLANDI": "Tamamlandı",
        "REDDEDILDI": "Reddedildi",
        "IPTAL_EDILDI": "İptal Edildi",
    }

    talep_durum_sayilari = {
        durum: 0
        for durum in talep_durum_adlari
    }

    talep_durum_sorgusu = (
        KiralamaTalebi.objects.filter(
            ilan__ilan_sahibi=request.user
        )
        .values("durum")
        .annotate(
            talep_sayisi=Count("id")
        )
    )

    for kayit in talep_durum_sorgusu:
        talep_durum_sayilari[kayit["durum"]] = (
            kayit["talep_sayisi"]
        )

    talep_grafik_etiketleri = [
        talep_durum_adlari[durum]
        for durum in talep_durum_adlari
    ]

    talep_grafik_verileri = [
        talep_durum_sayilari[durum]
        for durum in talep_durum_adlari
    ]

    # Kullanıcının ilanlarının kategori dağılımı
    kategori_sorgusu = (
        kullanici_ilanlari.values(
            "kategori__ad"
        )
        .annotate(
            ilan_sayisi=Count("id")
        )
        .order_by(
            "-ilan_sayisi",
            "kategori__ad",
        )[:6]
    )

    kategori_grafik_etiketleri = [
        kayit["kategori__ad"]
        for kayit in kategori_sorgusu
    ]

    kategori_grafik_verileri = [
        kayit["ilan_sayisi"]
        for kayit in kategori_sorgusu
    ]

    context = {
        "toplam_ilan_sayisi": kullanici_ilanlari.count(),
        "yayindaki_ilan_sayisi": kullanici_ilanlari.filter(
            durum="YAYINDA"
        ).count(),
        "bekleyen_talep_sayisi": KiralamaTalebi.objects.filter(
            ilan__ilan_sahibi=request.user,
            durum="BEKLIYOR",
        ).count(),
        "aktif_kiralama_sayisi": KiralamaTalebi.objects.filter(
            kiraci=request.user,
            durum__in=[
                "KABUL_EDILDI",
                "TESLIM_EDILDI",
                "IADE_EDILDI",
            ],
        ).count(),
        "son_ilanlar": son_ilanlar,
        "son_gelen_talepler": son_gelen_talepler,
        "ilan_grafik_etiketleri": ilan_grafik_etiketleri,
        "ilan_grafik_verileri": ilan_grafik_verileri,
        "talep_grafik_etiketleri": talep_grafik_etiketleri,
        "talep_grafik_verileri": talep_grafik_verileri,
        "kategori_grafik_etiketleri": kategori_grafik_etiketleri,
        "kategori_grafik_verileri": kategori_grafik_verileri,
    }

    return render(
        request,
        "accounts/panel.html",
        context,
    )