from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from rentals.models import KiralamaTalebi

from .forms import DegerlendirmeFormu
from .models import Degerlendirme


@login_required
def degerlendirme_olustur(request, talep_id):
    kiralama_talebi = get_object_or_404(
        KiralamaTalebi.objects.select_related(
            "ilan",
            "ilan__ilan_sahibi",
            "kiraci",
        ),
        id=talep_id,
        kiraci=request.user,
    )

    if kiralama_talebi.durum != "TAMAMLANDI":
        messages.error(
            request,
            "Yalnızca tamamlanmış kiralamalar değerlendirilebilir.",
        )

        return redirect(
            "rentals:benim_kiralama_taleplerim",
        )

    degerlendirme_var_mi = Degerlendirme.objects.filter(
        kiralama_talebi=kiralama_talebi,
    ).exists()

    if degerlendirme_var_mi:
        messages.warning(
            request,
            "Bu kiralama için daha önce değerlendirme yaptınız.",
        )

        return redirect(
            "rentals:benim_kiralama_taleplerim",
        )

    if request.method == "POST":
        form = DegerlendirmeFormu(
            request.POST,
        )

        if form.is_valid():
            degerlendirme = form.save(
                commit=False,
            )

            degerlendirme.kiralama_talebi = kiralama_talebi
            degerlendirme.degerlendiren = request.user
            degerlendirme.degerlendirilen = (
                kiralama_talebi.ilan.ilan_sahibi
            )

            degerlendirme.full_clean()
            degerlendirme.save()

            messages.success(
                request,
                "Değerlendirmeniz başarıyla kaydedildi.",
            )

            return redirect(
                "rentals:benim_kiralama_taleplerim",
            )

    else:
        form = DegerlendirmeFormu()

    return render(
        request,
        "reviews/degerlendirme_olustur.html",
        {
            "form": form,
            "kiralama_talebi": kiralama_talebi,
            "ilan": kiralama_talebi.ilan,
        },
    )