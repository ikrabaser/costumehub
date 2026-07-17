from django import forms

from .models import Ilan


class IlanFormu(forms.ModelForm):
    class Meta:
        model = Ilan

        fields = [
            "kategori",
            "baslik",
            "aciklama",
            "beden",
            "renk",
            "gunluk_fiyat",
            "depozito",
            "sehir",
        ]

        labels = {
            "kategori": "Kategori",
            "baslik": "İlan başlığı",
            "aciklama": "Açıklama",
            "beden": "Beden",
            "renk": "Renk",
            "gunluk_fiyat": "Günlük kiralama ücreti",
            "depozito": "Depozito",
            "sehir": "Şehir",
        }

        widgets = {
            "kategori": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "baslik": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Örneğin: Spider-Man cosplay kostümü",
                }
            ),
            "aciklama": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Kostümün durumu, kullanım bilgileri ve diğer detayları yazın",
                    "rows": 5,
                }
            ),
            "beden": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "renk": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Örneğin: Kırmızı - Mavi",
                }
            ),
            "gunluk_fiyat": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "depozito": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "sehir": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "İlanın bulunduğu şehir",
                }
            ),
        }

    def clean_gunluk_fiyat(self):
        gunluk_fiyat = self.cleaned_data["gunluk_fiyat"]

        if gunluk_fiyat <= 0:
            raise forms.ValidationError(
                "Günlük kiralama ücreti sıfırdan büyük olmalıdır."
            )

        return gunluk_fiyat

    def clean_depozito(self):
        depozito = self.cleaned_data["depozito"]

        if depozito < 0:
            raise forms.ValidationError(
                "Depozito negatif bir değer olamaz."
            )

        return depozito