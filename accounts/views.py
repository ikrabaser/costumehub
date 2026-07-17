from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def kayit_ol(request):
    if request.user.is_authenticated:
        return redirect("products:home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            kullanici = form.save()
            login(request, kullanici)

            messages.success(
                request,
                "Hesabınız başarıyla oluşturuldu."
            )

            return redirect("products:home")
    else:
        form = UserCreationForm()

    return render(
        request,
        "accounts/kayit.html",
        {"form": form}
    )


def giris_yap(request):
    if request.user.is_authenticated:
        return redirect("products:home")

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            kullanici = form.get_user()
            login(request, kullanici)

            messages.success(
                request,
                "Başarıyla giriş yaptınız."
            )

            return redirect("products:home")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/giris.html",
        {"form": form}
    )


def cikis_yap(request):
    logout(request)

    messages.success(
        request,
        "Hesabınızdan çıkış yaptınız."
    )

    return redirect("products:home")