from django import forms

from .models import KiralamaTalebi


class KiralamaTalebiFormu(forms.ModelForm):

    def __init__(self, *args, ilan=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ilan = ilan

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

    def clean(self):
        cleaned_data = super().clean()

        baslangic_tarihi = cleaned_data.get("baslangic_tarihi")
        bitis_tarihi = cleaned_data.get("bitis_tarihi")

        if not baslangic_tarihi or not bitis_tarihi:
            return cleaned_data

        if baslangic_tarihi > bitis_tarihi:
            raise forms.ValidationError(
                "Bitiş tarihi, başlangıç tarihinden önce olamaz."
            )

        if self.ilan:
            cakisan_talep_var_mi = (
                KiralamaTalebi.objects.filter(
                    ilan=self.ilan,
                    durum="KABUL_EDILDI",
                    baslangic_tarihi__lte=bitis_tarihi,
                    bitis_tarihi__gte=baslangic_tarihi,
                ).exists()
            )

            if cakisan_talep_var_mi:
                raise forms.ValidationError(
                    "Bu ilan seçtiğiniz tarihlerde daha önce kiralanmış."
                )

        return cleaned_data