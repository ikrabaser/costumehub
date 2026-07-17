from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import IlanFormu


def home(request):
    return render(request, "products/home.html")


@login_required
def ilan_olustur(request):
    if request.method == "POST":
        form = IlanFormu(request.POST)

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