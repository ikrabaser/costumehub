from django import forms

from .models import Ilan, Kategori


class CokluDosyaInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class CokluDosyaAlani(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget",
            CokluDosyaInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
        )
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        tek_dosya_temizle = super().clean

        if isinstance(data, (list, tuple)):
            return [
                tek_dosya_temizle(dosya, initial)
                for dosya in data
            ]

        if data:
            return [
                tek_dosya_temizle(data, initial)
            ]

        return []


class IlanFormu(forms.ModelForm):
    fotograflar = CokluDosyaAlani(
        required=False,
        label="İlan fotoğrafları",
        help_text=(
            "Birden fazla fotoğraf seçebilirsiniz. "
            "İlk seçilen fotoğraf ana fotoğraf olarak kullanılacaktır."
        ),
    )

    class Meta:
        model = Ilan

        fields = [
            "kategori",
            "baslik",
            "aciklama",
            "fotograflar",
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

    def clean_fotograflar(self):
        fotograflar = self.cleaned_data.get("fotograflar", [])

        en_fazla_fotograf_sayisi = 10
        en_fazla_dosya_boyutu = 5 * 1024 * 1024

        if len(fotograflar) > en_fazla_fotograf_sayisi:
            raise forms.ValidationError(
                "En fazla 10 fotoğraf yükleyebilirsiniz."
            )

        for fotograf in fotograflar:
            if fotograf.size > en_fazla_dosya_boyutu:
                raise forms.ValidationError(
                    "Her fotoğraf en fazla 5 MB olabilir."
                )

            if not fotograf.content_type.startswith("image/"):
                raise forms.ValidationError(
                    "Yalnızca görsel dosyaları yükleyebilirsiniz."
                )

        return fotograflar

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