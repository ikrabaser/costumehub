from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import IlanFormu
from .models import Ilan


def home(request):
    return render(request, "products/home.html")


@login_required
def ilan_olustur(request):
    if request.method == "POST":
        form = IlanFormu(request.POST)
        form = IlanFormu(
    request.POST,
    request.FILES
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
    ilanlar = Ilan.objects.filter(
        durum="YAYINDA",
        mevcut_mu=True
    ).select_related(
        "kategori",
        "ilan_sahibi"
    ).order_by("-olusturulma_tarihi")

    context = {
        "ilanlar": ilanlar
    }

    return render(
        request,
        "products/ilan_listesi.html",
        context
    )
def ilan_detay(request, ilan_id):
    ilan = get_object_or_404(
        Ilan.objects.select_related(
            "kategori",
            "ilan_sahibi",
            "ilan_sahibi__profil"
        ),
        id=ilan_id,
        durum="YAYINDA"
    )

    context = {
        "ilan": ilan
    }

    return render(
        request,
        "products/ilan_detay.html",
        context
    )