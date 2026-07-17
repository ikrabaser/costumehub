from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profil

class KayitFormu(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="E-posta adresi",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "ornek@email.com",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        labels = {
            "username": "Kullanıcı adı",
        }

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Kullanıcı adınızı girin",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].label = "Şifre"
        self.fields["password2"].label = "Şifre tekrarı"

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Şifrenizi girin",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Şifrenizi tekrar girin",
            }
        )


class GirisFormu(AuthenticationForm):
    username = forms.CharField(
        label="Kullanıcı adı",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Kullanıcı adınızı girin",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Şifre",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Şifrenizi girin",
            }
        ),
    )

class ProfilFormu(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ["telefon", "sehir", "biyografi"]

        labels = {
            "telefon": "Telefon",
            "sehir": "Şehir",
            "biyografi": "Biyografi",
        }

        widgets = {
            "telefon": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Telefon numaranızı girin",
                }
            ),
            "sehir": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Şehrinizi girin",
                }
            ),
            "biyografi": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Kendinizden kısaca bahsedin",
                    "rows": 4,
                }
            ),
        }