from django import forms

from .models import Ilan, Kategori


class IlanFormu(forms.ModelForm):
    class Meta:
        model = Ilan

        fields = [
            "kategori",
            "baslik",
            "aciklama",
            "fotograf",
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
            "fotograf": "İlan fotoğrafı",
            "beden": "Beden",
            "renk": "Renk",
            "gunluk_fiyat": "Günlük kiralama ücreti",
            "depozito": "Depozito",
            "sehir": "Şehir",
        }

        widgets = {
            "kategori": forms.HiddenInput(
                attrs={
                    "id": "id_kategori",
                }
            ),
            "baslik": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "Örneğin: Spider-Man cosplay kostümü"
                    ),
                }
            ),
            "aciklama": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "Kostümün durumu, kullanım bilgileri "
                        "ve diğer detayları yazın"
                    ),
                    "rows": 5,
                }
            ),
            "fotograf": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
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
                    "min": "0.01",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["kategori"].queryset = (
            Kategori.objects.filter(
                aktif_mi=True,
            )
            .select_related(
                "ust_kategori",
            )
            .order_by(
                "sira",
                "ad",
            )
        )

    def clean_kategori(self):
        kategori = self.cleaned_data.get("kategori")

        if kategori is None:
            raise forms.ValidationError(
                "Lütfen ilan için bir kategori seçin."
            )

        if not kategori.aktif_mi:
            raise forms.ValidationError(
                "Seçtiğiniz kategori artık aktif değildir."
            )

        aktif_alt_kategori_var_mi = (
            kategori.alt_kategoriler.filter(
                aktif_mi=True,
            ).exists()
        )

        if aktif_alt_kategori_var_mi:
            raise forms.ValidationError(
                "İlanı bir ara kategoriye ekleyemezsiniz. "
                "Lütfen en alt kategoriyi seçin."
            )

        return kategori

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