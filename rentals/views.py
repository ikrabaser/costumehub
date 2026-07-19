from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

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
@require_POST
def kiralama_talebi_kabul_et(request, talep_id):
    talep = get_object_or_404(
        KiralamaTalebi,
        id=talep_id,
        ilan__ilan_sahibi=request.user,
        durum="BEKLIYOR",
    )

    tarih_cakismasi_var_mi = (
        KiralamaTalebi.objects.filter(
            ilan=talep.ilan,
            durum__in=[
                "KABUL_EDILDI",
                "TESLIM_EDILDI",
                "IADE_EDILDI",
                "TAMAMLANDI",
            ],
            baslangic_tarihi__lte=talep.bitis_tarihi,
            bitis_tarihi__gte=talep.baslangic_tarihi,
        )
        .exclude(id=talep.id)
        .exists()
    )

    if tarih_cakismasi_var_mi:
        messages.error(
            request,
            (
                "Bu tarihler için daha önce kabul edilmiş "
                "başka bir kiralama bulunmaktadır."
            ),
        )

        return redirect(
            "rentals:gelen_kiralama_talepleri",
        )

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
@require_POST
def kiralama_talebi_reddet(request, talep_id):
    talep = get_object_or_404(
        KiralamaTalebi,
        id=talep_id,
        ilan__ilan_sahibi=request.user,
        durum="BEKLIYOR",
    )

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
@require_POST
def kiralama_talebi_teslim_et(request, talep_id):
    talep = get_object_or_404(
        KiralamaTalebi,
        id=talep_id,
        ilan__ilan_sahibi=request.user,
        durum="KABUL_EDILDI",
    )

    talep.durum = "TESLIM_EDILDI"

    talep.save(
        update_fields=[
            "durum",
            "guncellenme_tarihi",
        ]
    )

    messages.success(
        request,
        "Ürün kiracıya teslim edildi olarak işaretlendi.",
    )

    return redirect(
        "rentals:gelen_kiralama_talepleri",
    )


@login_required
@require_POST
def kiralama_talebi_iade_al(request, talep_id):
    talep = get_object_or_404(
        KiralamaTalebi,
        id=talep_id,
        ilan__ilan_sahibi=request.user,
        durum="TESLIM_EDILDI",
    )

    talep.durum = "IADE_EDILDI"

    talep.save(
        update_fields=[
            "durum",
            "guncellenme_tarihi",
        ]
    )

    messages.success(
        request,
        "Ürün iade alındı olarak işaretlendi.",
    )

    return redirect(
        "rentals:gelen_kiralama_talepleri",
    )


@login_required
@require_POST
def kiralama_talebi_tamamla(request, talep_id):
    talep = get_object_or_404(
        KiralamaTalebi,
        id=talep_id,
        ilan__ilan_sahibi=request.user,
        durum="IADE_EDILDI",
    )

    talep.durum = "TAMAMLANDI"

    talep.save(
        update_fields=[
            "durum",
            "guncellenme_tarihi",
        ]
    )

    messages.success(
        request,
        "Kiralama süreci tamamlandı.",
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