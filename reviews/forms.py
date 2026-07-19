from django import forms

from .models import Degerlendirme


PUAN_SECENEKLERI = [
    (1, "1 ⭐"),
    (2, "2 ⭐⭐"),
    (3, "3 ⭐⭐⭐"),
    (4, "4 ⭐⭐⭐⭐"),
    (5, "5 ⭐⭐⭐⭐⭐"),
]



class DegerlendirmeFormu(forms.ModelForm):

    class Meta:
        model = Degerlendirme

        fields = [
            "puan",
            "yorum",
        ]

        labels = {
            "puan": "Puanınız",
            "yorum": "Yorumunuz",
        }

        widgets = {
            "puan": forms.RadioSelect(
                choices=PUAN_SECENEKLERI,
            ),
            "yorum": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "maxlength": 1000,
                    "placeholder": (
                        "Kostümün durumu, ilan sahibiyle iletişim "
                        "ve kiralama deneyiminiz hakkında yazabilirsiniz."
                    ),
                }
            ),
        }

    def clean_yorum(self):
        yorum = self.cleaned_data.get(
            "yorum",
            "",
        ).strip()

        if not yorum:
            raise forms.ValidationError(
                "Lütfen değerlendirme yorumunuzu yazın."
            )

        if len(yorum) < 10:
            raise forms.ValidationError(
                "Yorumunuz en az 10 karakter olmalıdır."
            )

        return yorum