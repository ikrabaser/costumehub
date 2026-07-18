from django import forms

from .models import KiralamaTalebi


class KiralamaTalebiFormu(forms.ModelForm):

    class Meta:
        model = KiralamaTalebi

        fields = [
            "baslangic_tarihi",
            "bitis_tarihi",
            "not_metni",
        ]

        widgets = {
            "baslangic_tarihi": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "bitis_tarihi": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "not_metni": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "İlan sahibine iletmek istediğiniz "
                        "bir not varsa yazabilirsiniz."
                    ),
                }
            ),
        }