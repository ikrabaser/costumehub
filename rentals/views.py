from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date
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

    oturum_anahtari = (
        f"kiralama_tarihleri_{ilan.id}"
    )

    if request.method == "GET":
        baslangic_tarihi_metni = request.GET.get(
            "baslangic",
            "",
        ).strip()

        bitis_tarihi_metni = request.GET.get(
            "bitis",
            "",
        ).strip()

        baslangic_tarihi = parse_date(
            baslangic_tarihi_metni
        )

        bitis_tarihi = parse_date(
            bitis_tarihi_metni
        )

        if not baslangic_tarihi or not bitis_tarihi:
            messages.error(
                request,
                (
                    "Lütfen kiralama tarihlerini "
                    "ilan takviminden seçin."
                ),
            )

            return redirect(
                "products:ilan_detay",
                ilan_id=ilan.id,
            )

        request.session[oturum_anahtari] = {
            "baslangic": baslangic_tarihi.isoformat(),
            "bitis": bitis_tarihi.isoformat(),
        }

        form = KiralamaTalebiFormu(
            ilan=ilan,
            initial={
                "baslangic_tarihi": baslangic_tarihi,
                "bitis_tarihi": bitis_tarihi,
            },
        )

    else:
        oturum_tarihleri = request.session.get(
            oturum_anahtari
        )

        if not oturum_tarihleri:
            messages.error(
                request,
                (
                    "Kiralama tarihi seçiminizin süresi dolmuş. "
                    "Lütfen tarihleri yeniden seçin."
                ),
            )

            return redirect(
                "products:ilan_detay",
                ilan_id=ilan.id,
            )

        baslangic_tarihi = parse_date(
            oturum_tarihleri.get(
                "baslangic",
                "",
            )
        )

        bitis_tarihi = parse_date(
            oturum_tarihleri.get(
                "bitis",
                "",
            )
        )

        form_verileri = request.POST.copy()

        form_verileri["baslangic_tarihi"] = (
            baslangic_tarihi.isoformat()
            if baslangic_tarihi
            else ""
        )

        form_verileri["bitis_tarihi"] = (
            bitis_tarihi.isoformat()
            if bitis_tarihi
            else ""
        )

        form = KiralamaTalebiFormu(
            form_verileri,
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

            request.session.pop(
                oturum_anahtari,
                None,
            )

            messages.success(
                request,
                "Kiralama talebiniz başarıyla oluşturuldu.",
            )

            return redirect(
                "products:ilan_detay",
                ilan_id=ilan.id,
            )

    toplam_gun = (
        bitis_tarihi - baslangic_tarihi
    ).days + 1

    toplam_tutar = (
        Decimal(toplam_gun)
        * ilan.gunluk_fiyat
    )

    return render(
        request,
        "rentals/kiralama_talebi_olustur.html",
        {
            "form": form,
            "ilan": ilan,
            "baslangic_tarihi": baslangic_tarihi,
            "bitis_tarihi": bitis_tarihi,
            "toplam_gun": toplam_gun,
            "toplam_tutar": toplam_tutar,
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
            "degerlendirme",
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