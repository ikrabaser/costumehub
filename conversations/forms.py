from django import forms

from .models import Mesaj


class MesajFormu(forms.ModelForm):

    class Meta:
        model = Mesaj

        fields = [
            "icerik",
        ]

        labels = {
            "icerik": "",
        }

        widgets = {
            "icerik": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Mesajınızı yazın...",
                    "maxlength": 1000,
                }
            ),
        }

    def clean_icerik(self):
        icerik = self.cleaned_data.get(
            "icerik",
            "",
        ).strip()

        if not icerik:
            raise forms.ValidationError(
                "Mesaj alanı boş bırakılamaz."
            )

        return icerik