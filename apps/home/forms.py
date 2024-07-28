from django import forms
from .models import MusteriKayit,Sac,Boya,Yatak,MotorReduktor,Profil,Isleme,TeknolojikAlim
import uuid


class MusteriKayitForm(forms.ModelForm):
    class Meta:
        model = MusteriKayit
        fields = ['musteri_adi', 'adres', 'telefon', 'email','aciklama','proje_kodu','proje_genel','created_by']


class SacForm(forms.ModelForm):
    class Meta:
        model = Sac
        fields = [
            'projekodu','kalinlik', 'boy', 'en', 'adet','olusturma_tarih',
            'kalite', 'depo_secimi', 'giris_aciklama', 'created_by','musteri',
        ]
    def clean_projekodu(self):
        projekodu = self.cleaned_data.get('projekodu')
        try:
            musteri_kayit = MusteriKayit.objects.get(proje_kodu=projekodu)
        except MusteriKayit.DoesNotExist:
            raise forms.ValidationError(f"Proje kodu '{projekodu}' bulunamadı.")
        return musteri_kayit


class BoyaForm(forms.ModelForm):
    class Meta:
        model = Boya
        fields = [
            'projekodu','marka', 'cinsi', 'adet','renk','olusturma_tarih',
            'kalite', 'depo_secimi', 'giris_aciklama', 'created_by','musteri',
        ]
    def clean_projekodu(self):
        projekodu = self.cleaned_data.get('projekodu')
        try:
            musteri_kayit = MusteriKayit.objects.get(proje_kodu=projekodu)
        except MusteriKayit.DoesNotExist:
            raise forms.ValidationError(f"Proje kodu '{projekodu}' bulunamadı.")
        return musteri_kayit

class YatakForm(forms.ModelForm):
    class Meta:
        model = Yatak
        fields = [
            'projekodu','marka', 'yatak_kodu', 'adet', 'olusturma_tarih','depo_secimi', 'giris_aciklama', 'created_by','musteri',
        ]
    def clean_projekodu(self):
        projekodu = self.cleaned_data.get('projekodu')
        try:
            musteri_kayit = MusteriKayit.objects.get(proje_kodu=projekodu)
        except MusteriKayit.DoesNotExist:
            raise forms.ValidationError(f"Proje kodu '{projekodu}' bulunamadı.")
        return musteri_kayit
    
class MotorForm(forms.ModelForm):
    class Meta:
        model = MotorReduktor
        fields = [
            'projekodu','marka', 'kw', 'adet','devir', 'olusturma_tarih','depo_secimi', 'giris_aciklama', 'created_by','musteri',
        ]
    def clean_projekodu(self):
        projekodu = self.cleaned_data.get('projekodu')
        try:
            musteri_kayit = MusteriKayit.objects.get(proje_kodu=projekodu)
        except MusteriKayit.DoesNotExist:
            raise forms.ValidationError(f"Proje kodu '{projekodu}' bulunamadı.")
        return musteri_kayit


class ProfilForm(forms.ModelForm):
    #olusturma_tarih = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Profil
        fields = [
            'projekodu','kalinlik', 'boy','adet','olusturma_tarih','kalite', 'depo_secimi', 'giris_aciklama', 'created_by','musteri'
        ]
    def clean_projekodu(self):
        projekodu = self.cleaned_data.get('projekodu')
        try:
            musteri_kayit = MusteriKayit.objects.get(proje_kodu=projekodu)
        except MusteriKayit.DoesNotExist:
            raise forms.ValidationError(f"Proje kodu '{projekodu}' bulunamadı.")
        return musteri_kayit

class IslemeForm(forms.ModelForm):
    #olusturma_tarih = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Isleme
        fields = [
            'projekodu', 'cinsi','adet','olusturma_tarih','yer', 'depo_secimi', 'giris_aciklama', 'created_by','musteri'
        ]
    def clean_projekodu(self):
        projekodu = self.cleaned_data.get('projekodu')
        try:
            musteri_kayit = MusteriKayit.objects.get(proje_kodu=projekodu)
        except MusteriKayit.DoesNotExist:
            raise forms.ValidationError(f"Proje kodu '{projekodu}' bulunamadı.")
        return musteri_kayit

class TeknolojiForm(forms.ModelForm):
    #olusturma_tarih = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = TeknolojikAlim
        fields = [
            'projekodu', 'malzeme_tipi','malzeme_adi','adet','olusturma_tarih', 'depo_secimi', 'giris_aciklama', 'created_by','musteri'
        ]
    def clean_projekodu(self):
        projekodu = self.cleaned_data.get('projekodu')
        try:
            musteri_kayit = MusteriKayit.objects.get(proje_kodu=projekodu)
        except MusteriKayit.DoesNotExist:
            raise forms.ValidationError(f"Proje kodu '{projekodu}' bulunamadı.")
        return musteri_kayit