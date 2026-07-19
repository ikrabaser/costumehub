from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Ilan

from .forms import KiralamaTalebiFormu
from .models import KiralamaTalebi


@login_required
def kiralama_talebi_olustur(request, ilan_id):
    ilan = get_object_or_404(
        Ilan,
        id=ilan_id,
        durum="YAYINDA",
        mevcut_mu=True,
    )

    if ilan.ilan_sahibi == request.user:
        messages.error(
            request,
            "Kendi ilanınız için kiralama talebi oluşturamazsınız.",
        )

        return redirect(
            "products:ilan_detay",
            ilan_id=ilan.id,
        )

    if request.method == "POST":
        form = KiralamaTalebiFormu(
            request.POST,
            ilan=ilan,
        )

        if form.is_valid():
            talep = form.save(commit=False)

            toplam_gun = (
                talep.bitis_tarihi
                - talep.baslangic_tarihi
            ).days + 1

            talep.ilan = ilan
            talep.kiraci = request.user
            talep.toplam_gun = toplam_gun
            talep.toplam_tutar = (
                Decimal(toplam_gun)
                * ilan.gunluk_fiyat
            )

            talep.full_clean()
            talep.save()

            messages.success(
                request,
                "Kiralama talebiniz başarıyla oluşturuldu.",
            )

            return redirect(
                "products:ilan_detay",
                ilan_id=ilan.id,
            )

    else:
        form = KiralamaTalebiFormu(
            ilan=ilan,
        )

    return render(
        request,
        "rentals/kiralama_talebi_olustur.html",
        {
            "form": form,
            "ilan": ilan,
        },
    )


@login_required
def gelen_kiralama_talepleri(request):
    talepler = (
        KiralamaTalebi.objects.filter(
            ilan__ilan_sahibi=request.user,
        )
        .select_related(
            "ilan",
            "kiraci",
        )
        .order_by("-olusturulma_tarihi")
    )

    return render(
        request,
        "rentals/gelen_kiralama_talepleri.html",
        {
            "talepler": talepler,
        },
    )


@login_required
def kiralama_talebi_kabul_et(request, talep_id):
    talep = get_object_or_404(
        KiralamaTalebi,
        id=talep_id,
        ilan__ilan_sahibi=request.user,
        durum="BEKLIYOR",
    )

    if request.method == "POST":
        talep.durum = "KABUL_EDILDI"

        talep.save(
            update_fields=[
                "durum",
                "guncellenme_tarihi",
            ]
        )

        messages.success(
            request,
            "Kiralama talebi kabul edildi.",
        )

    return redirect(
        "rentals:gelen_kiralama_talepleri",
    )


@login_required
def kiralama_talebi_reddet(request, talep_id):
    talep = get_object_or_404(
        KiralamaTalebi,
        id=talep_id,
        ilan__ilan_sahibi=request.user,
        durum="BEKLIYOR",
    )

    if request.method == "POST":
        talep.durum = "REDDEDILDI"

        talep.save(
            update_fields=[
                "durum",
                "guncellenme_tarihi",
            ]
        )

        messages.success(
            request,
            "Kiralama talebi reddedildi.",
        )

    return redirect(
        "rentals:gelen_kiralama_talepleri",
    )


@login_required
def benim_kiralama_taleplerim(request):
    talepler = (
        KiralamaTalebi.objects.filter(
            kiraci=request.user,
        )
        .select_related(
            "ilan",
            "ilan__ilan_sahibi",
        )
        .order_by("-olusturulma_tarihi")
    )

    return render(
        request,
        "rentals/benim_kiralama_taleplerim.html",
        {
            "talepler": talepler,
        },
    )