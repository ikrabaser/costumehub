from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import GirisFormu, KayitFormu, ProfilFormu


def kayit(request):
    if request.user.is_authenticated:
        return redirect("accounts:panel")

    if request.method == "POST":
        form = KayitFormu(request.POST)

        if form.is_valid():
            kullanici = form.save()
            login(request, kullanici)

            messages.success(
                request,
                "Hesabınız başarıyla oluşturuldu. CostumeHub'a hoş geldiniz!",
            )

            return redirect("accounts:panel")
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
        return redirect("accounts:panel")

    if request.method == "POST":
        form = GirisFormu(request, data=request.POST)

        if form.is_valid():
            kullanici = form.get_user()
            login(request, kullanici)

            messages.success(
                request,
                f"Hoş geldiniz, {kullanici.username}!",
            )

            return redirect("accounts:panel")
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

@login_required
def profil(request):
    profil_nesnesi = request.user.profil

    if request.method == "POST":
        form = ProfilFormu(
            request.POST,
            instance=profil_nesnesi,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Profil bilgileriniz başarıyla güncellendi.",
            )

            return redirect("accounts:profil")
    else:
        form = ProfilFormu(instance=profil_nesnesi)

    return render(
        request,
        "accounts/profil.html",
        {
            "profil": profil_nesnesi,
            "form": form,
        },
    )
@login_required
def panel(request):
    return render(
        request,
        "accounts/panel.html",
    )