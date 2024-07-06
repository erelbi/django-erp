from django import forms
from .models import MusteriKayit

class MusteriKayitForm(forms.ModelForm):
    class Meta:
        model = MusteriKayit
        fields = ['musteri_adi', 'musteri_kodu', 'adres', 'telefon', 'email']