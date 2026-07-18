from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Ilan

from .forms import KiralamaTalebiFormu


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
            "Kendi ilanınız için kiralama talebi oluşturamazsınız."
        )

        return redirect(
            "products:ilan_detay",
            ilan_id=ilan.id
        )

    if request.method == "POST":
        form = KiralamaTalebiFormu(request.POST)

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
                "Kiralama talebiniz başarıyla oluşturuldu."
            )

            return redirect(
                "products:ilan_detay",
                ilan_id=ilan.id
            )

    else:
        form = KiralamaTalebiFormu()

    return render(
        request,
        "rentals/kiralama_talebi_olustur.html",
        {
            "form": form,
            "ilan": ilan,
        }
    )