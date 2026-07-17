from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import GirisFormu, KayitFormu


def kayit(request):
    if request.user.is_authenticated:
        return redirect("products:home")

    if request.method == "POST":
        form = KayitFormu(request.POST)

        if form.is_valid():
            kullanici = form.save()
            login(request, kullanici)

            messages.success(
                request,
                "Hesabınız başarıyla oluşturuldu. CostumeHub'a hoş geldiniz!",
            )

            return redirect("products:home")
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
        return redirect("products:home")

    if request.method == "POST":
        form = GirisFormu(request, data=request.POST)

        if form.is_valid():
            kullanici = form.get_user()
            login(request, kullanici)

            messages.success(
                request,
                f"Hoş geldiniz, {kullanici.username}!",
            )

            return redirect("products:home")
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