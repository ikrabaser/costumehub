from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect,render
from django.views.decorators.http import require_POST

from products.models import Ilan
from .models import Favori


@login_required
@require_POST
def favori_degistir(request, ilan_id):
    ilan = get_object_or_404(Ilan, id=ilan_id)

    favori, olusturuldu = Favori.objects.get_or_create(
        kullanici=request.user,
        ilan=ilan,
    )

    if not olusturuldu:
        favori.delete()

    return redirect(
        "products:ilan_detay",
        ilan_id=ilan.id,
    )
@login_required
def favorilerim(request):
    favoriler = Favori.objects.filter(
        kullanici=request.user,
    ).select_related(
        "ilan",
        "ilan__kategori",
        "ilan__ilan_sahibi",
    )

    context = {
        "favoriler": favoriler,
    }

    return render(
        request,
        "favorites/favorilerim.html",
        context,
    )