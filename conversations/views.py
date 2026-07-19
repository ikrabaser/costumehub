from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Ilan

from .forms import MesajFormu
from .models import Mesaj, Sohbet


@login_required
def sohbet_baslat(request, ilan_id):
    ilan = get_object_or_404(
        Ilan,
        id=ilan_id,
        durum="YAYINDA",
        mevcut_mu=True,
    )

    if ilan.ilan_sahibi == request.user:
        messages.error(
            request,
            "Kendi ilanınız için sohbet başlatamazsınız.",
        )

        return redirect(
            "products:ilan_detay",
            ilan_id=ilan.id,
        )

    sohbet, olusturuldu_mu = Sohbet.objects.get_or_create(
        ilan=ilan,
        kiraci=request.user,
        defaults={
            "ilan_sahibi": ilan.ilan_sahibi,
        },
    )

    if olusturuldu_mu:
        sohbet.full_clean()
        sohbet.save()

    return redirect(
        "conversations:sohbet_detay",
        sohbet_id=sohbet.id,
    )


@login_required
def sohbet_listesi(request):
    sohbetler = (
        Sohbet.objects.filter(
            Q(kiraci=request.user)
            | Q(ilan_sahibi=request.user)
        )
        .select_related(
            "ilan",
            "kiraci",
            "ilan_sahibi",
        )
        .prefetch_related(
            "mesajlar",
        )
        .distinct()
    )

    return render(
        request,
        "conversations/sohbet_listesi.html",
        {
            "sohbetler": sohbetler,
        },
    )


@login_required
def sohbet_detay(request, sohbet_id):
    sohbet = get_object_or_404(
        Sohbet.objects.select_related(
            "ilan",
            "kiraci",
            "ilan_sahibi",
        ),
        id=sohbet_id,
    )

    izinli_mi = (
        request.user == sohbet.kiraci
        or request.user == sohbet.ilan_sahibi
    )

    if not izinli_mi:
        messages.error(
            request,
            "Bu sohbete erişim yetkiniz bulunmuyor.",
        )

        return redirect(
            "conversations:sohbet_listesi",
        )

    okunmamis_mesajlar = sohbet.mesajlar.exclude(
        gonderen=request.user,
    ).filter(
        okundu_mu=False,
    )

    okunmamis_mesajlar.update(
        okundu_mu=True,
    )

    if request.method == "POST":
        form = MesajFormu(
            request.POST,
        )

        if form.is_valid():
            mesaj = form.save(
                commit=False,
            )

            mesaj.sohbet = sohbet
            mesaj.gonderen = request.user

            mesaj.full_clean()
            mesaj.save()

            sohbet.save(
                update_fields=[
                    "guncellenme_tarihi",
                ]
            )

            return redirect(
                "conversations:sohbet_detay",
                sohbet_id=sohbet.id,
            )

    else:
        form = MesajFormu()

    mesajlar = sohbet.mesajlar.select_related(
        "gonderen",
    ).all()

    return render(
        request,
        "conversations/sohbet_detay.html",
        {
            "sohbet": sohbet,
            "mesajlar": mesajlar,
            "form": form,
        },
    )