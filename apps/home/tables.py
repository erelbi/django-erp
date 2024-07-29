# myapp/tables.py
import django_tables2 as tables
from .models import Sac, Boya, Yatak, MotorReduktor, Profil, Isleme, TeknolojikAlim



class SacTable(tables.Table):
    class Meta:
        model = Sac
        fields = ('stok_kodu', 'musteri', 'kalinlik', 'boy', 'en', 'adet', 'kalite', 'depo_secimi', 'olusturma_tarih', 'son_edit_tarih', 'created_by', 'updated_by', 'giris_aciklama', 'cikis_aciklama')

class BoyaTable(tables.Table):
    class Meta:
        model = Boya
        fields = ('stok_kodu', 'musteri', 'renk', 'marka', 'cinsi', 'adet', 'kalite', 'depo_secimi', 'olusturma_tarih', 'son_edit_tarih', 'created_by', 'updated_by', 'giris_aciklama', 'cikis_aciklama')

class YatakTable(tables.Table):
    class Meta:
        model = Yatak
        fields = ('stok_kodu', 'musteri', 'marka', 'adet', 'yatak_kodu', 'depo_secimi', 'olusturma_tarih', 'son_edit_tarih', 'created_by', 'updated_by', 'giris_aciklama', 'cikis_aciklama')

class MotorReduktorTable(tables.Table):
    class Meta:
        model = MotorReduktor
        fields = ('stok_kodu', 'musteri', 'marka', 'kw', 'devir', 'adet', 'depo_secimi', 'olusturma_tarih', 'son_edit_tarih', 'created_by', 'updated_by', 'giris_aciklama', 'cikis_aciklama')

class ProfilTable(tables.Table):
    class Meta:
        model = Profil
        fields = ('stok_kodu', 'musteri', 'kalinlik', 'boy', 'adet', 'kalite', 'depo_secimi', 'olusturma_tarih', 'son_edit_tarih', 'created_by', 'updated_by', 'giris_aciklama', 'cikis_aciklama')

class IslemeTable(tables.Table):
    class Meta:
        model = Isleme
        fields = ('stok_kodu', 'musteri', 'cinsi', 'yer', 'adet', 'depo_secimi', 'olusturma_tarih', 'son_edit_tarih', 'created_by', 'updated_by', 'giris_aciklama', 'cikis_aciklama')

class TeknolojikAlimTable(tables.Table):
    class Meta:
        model = TeknolojikAlim
        fields = ('stok_kodu', 'musteri', 'malzeme_tipi', 'malzeme_adi', 'adet', 'depo_secimi', 'olusturma_tarih', 'son_edit_tarih', 'created_by', 'updated_by', 'giris_aciklama', 'cikis_aciklama')
