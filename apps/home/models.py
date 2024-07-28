# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


import uuid

class MusteriKayit(models.Model):
    musteri_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    musteri_adi = models.CharField(max_length=255)
    adres = models.TextField()
    telefon = models.CharField(max_length=20)
    email = models.EmailField()
    aciklama = models.TextField(null=True, blank=True)
    proje_kodu = models.CharField(max_length=255,unique=True)
    proje_genel = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='created_musteri', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_musteri', on_delete=models.SET_NULL, null=True, blank=True)
    proje_tarihi = models.DateTimeField(auto_now_add=True) 

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['proje_kodu'], name='unique_proje_kodu')
        ]

    def __str__(self):
         return self.proje_kodu




class DepoHareket(models.Model):
    proje_kodu = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE,to_field='proje_kodu')
    musteri = models.CharField(max_length=255)
    tarih = models.DateTimeField(auto_now=True)
    depo = models.CharField(max_length=255)
    stok_kodu = models.CharField(max_length=255)

    def __str__(self):
        return self.stok_kodu

class Sac(models.Model):
    musteri = models.CharField(max_length=255)
    stok_kodu = models.CharField(max_length=255)
    projekodu = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE,to_field='proje_kodu')
    kalinlik = models.FloatField(null=True, blank=True)
    boy = models.FloatField(null=True, blank=True)
    en = models.FloatField(null=True, blank=True)
    adet = models.IntegerField()
    kalite = models.CharField(max_length=255)
    depo_secimi = models.CharField(max_length=255)
    olusturma_tarih = models.DateTimeField(null=True)
    son_edit_tarih = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='created_sac', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_sac', on_delete=models.SET_NULL, null=True, blank=True)
    giris_aciklama = models.TextField(null=True, blank=True)
    cikis_aciklama = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        
        if not self.stok_kodu:
            last_stok_kodu = Sac.objects.all().order_by('id').last()
            if last_stok_kodu:
                last_number = int(last_stok_kodu.stok_kodu.split('stksac')[-1])
                self.stok_kodu = f'stksac{last_number + 1}'
            else:
                self.stok_kodu = 'stksac1'


        super(Sac, self).save(*args, **kwargs)

    def __str__(self):
        return self.stok_kodu
    
class Boya(models.Model):
    musteri = models.CharField(max_length=255)
    stok_kodu = models.CharField(max_length=255)
    projekodu = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE,to_field='proje_kodu')
    renk = models.CharField(max_length=255)
    marka = models.CharField(max_length=255)
    cinsi = models.CharField(max_length=255)
    adet = models.IntegerField()
    kalite = models.CharField(max_length=255)
    depo_secimi = models.CharField(max_length=255)
    olusturma_tarih = models.DateTimeField(null=True)
    son_edit_tarih = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='created_boya', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_boya', on_delete=models.SET_NULL, null=True, blank=True)
    giris_aciklama = models.TextField(null=True, blank=True)
    cikis_aciklama = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        
        if not self.stok_kodu:
            last_stok_kodu = Boya.objects.all().order_by('id').last()
            if last_stok_kodu:
                last_number = int(last_stok_kodu.stok_kodu.split('stkby')[-1])
                self.stok_kodu = f'stkby{last_number + 1}'
            else:
                self.stok_kodu = 'stkby1'


        super(Boya, self).save(*args, **kwargs)

    def __str__(self):
        return self.stok_kodu


class Yatak(models.Model):
    musteri = models.CharField(max_length=255)
    stok_kodu = models.CharField(max_length=255)
    projekodu = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE,to_field='proje_kodu')
    marka = models.CharField(max_length=255)
    adet = models.IntegerField()
    yatak_kodu = models.CharField(max_length=255)
    depo_secimi = models.CharField(max_length=255)
    olusturma_tarih = models.DateTimeField(null=True)
    son_edit_tarih = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='created_yatak', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_yatak', on_delete=models.SET_NULL, null=True, blank=True)
    giris_aciklama = models.TextField(null=True, blank=True)
    cikis_aciklama = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        
        if not self.stok_kodu:
            last_stok_kodu = Yatak.objects.all().order_by('id').last()
            if last_stok_kodu:
                last_number = int(last_stok_kodu.stok_kodu.split('stkytk')[-1])
                self.stok_kodu = f'stkytk{last_number + 1}'
            else:
                self.stok_kodu = 'stkytk1'


        super(Yatak, self).save(*args, **kwargs)

    def __str__(self):
        return self.stok_kodu


class MotorReduktor(models.Model):
    musteri = models.CharField(max_length=255)
    stok_kodu = models.CharField(max_length=255)
    projekodu = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE,to_field='proje_kodu')
    marka = models.CharField(max_length=255)
    kw = models.DecimalField(max_digits=10, decimal_places=2)
    devir = models.DecimalField(max_digits=10, decimal_places=2)
    adet = models.IntegerField()
    depo_secimi = models.CharField(max_length=255)
    olusturma_tarih = models.DateTimeField(null=True)
    son_edit_tarih = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='created_motor', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_motor', on_delete=models.SET_NULL, null=True, blank=True)
    giris_aciklama = models.TextField(null=True, blank=True)
    cikis_aciklama = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        
        if not self.stok_kodu:
            last_stok_kodu = MotorReduktor.objects.all().order_by('id').last()
            if last_stok_kodu:
                last_number = int(last_stok_kodu.stok_kodu.split('stkmtr')[-1])
                self.stok_kodu = f'stkmtr{last_number + 1}'
            else:
                self.stok_kodu = 'stkmtr1'


        super(MotorReduktor, self).save(*args, **kwargs)

    def __str__(self):
        return self.stok_kodu

class Profil(models.Model):
    musteri = models.CharField(max_length=255)
    stok_kodu = models.CharField(max_length=255)
    projekodu = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE,to_field='proje_kodu')
    kalinlik = models.FloatField(null=True, blank=True)
    boy = models.FloatField(null=True, blank=True)
    adet = models.IntegerField()
    kalite = models.CharField(max_length=255)
    depo_secimi = models.CharField(max_length=255)
    olusturma_tarih = models.DateTimeField(null=True)
    son_edit_tarih = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='created_profil', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_profil', on_delete=models.SET_NULL, null=True, blank=True)
    giris_aciklama = models.TextField(null=True, blank=True)
    cikis_aciklama = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        
        if not self.stok_kodu:
            last_stok_kodu = Profil.objects.all().order_by('id').last()
            if last_stok_kodu:
                last_number = int(last_stok_kodu.stok_kodu.split('stkprfl')[-1])
                self.stok_kodu = f'stkprfl{last_number + 1}'
            else:
                self.stok_kodu = 'stkprfl1'


        super(Profil, self).save(*args, **kwargs)

    def __str__(self):
        return self.stok_kodu

class Isleme(models.Model):
    musteri = models.CharField(max_length=255)
    stok_kodu = models.CharField(max_length=255)
    projekodu = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE,to_field='proje_kodu')
    cinsi = models.CharField(max_length=255)
    yer = models.CharField(max_length=255)
    adet = models.IntegerField()
    depo_secimi = models.CharField(max_length=255)
    olusturma_tarih = models.DateTimeField(null=True)
    son_edit_tarih = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='created_isleme', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_isleme', on_delete=models.SET_NULL, null=True, blank=True)
    giris_aciklama = models.TextField(null=True, blank=True)
    cikis_aciklama = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        
        if not self.stok_kodu:
            last_stok_kodu = Isleme.objects.all().order_by('id').last()
            if last_stok_kodu:
                last_number = int(last_stok_kodu.stok_kodu.split('stkislm')[-1])
                self.stok_kodu = f'stkislm{last_number + 1}'
            else:
                self.stok_kodu = 'stkislm1'


        super(Isleme, self).save(*args, **kwargs)

    def __str__(self):
        return self.stok_kodu

class TeknolojikAlim(models.Model):
    musteri = models.CharField(max_length=255)
    stok_kodu = models.CharField(max_length=255)
    projekodu = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE,to_field='proje_kodu')
    malzeme_tipi = models.CharField(max_length=255)
    malzeme_adi = models.CharField(max_length=255)
    adet = models.IntegerField()
    depo_secimi = models.CharField(max_length=255)
    olusturma_tarih = models.DateTimeField(null=True)
    son_edit_tarih = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='created_teknoloji', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='updated_teknoloji', on_delete=models.SET_NULL, null=True, blank=True)
    giris_aciklama = models.TextField(null=True, blank=True)
    cikis_aciklama = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        
        if not self.stok_kodu:
            last_stok_kodu = TeknolojikAlim.objects.all().order_by('id').last()
            if last_stok_kodu:
                last_number = int(last_stok_kodu.stok_kodu.split('stktknlj')[-1])
                self.stok_kodu = f'stktknlj{last_number + 1}'
            else:
                self.stok_kodu = 'stktknlj1'


        super(TeknolojikAlim, self).save(*args, **kwargs)

    def __str__(self):
        return self.stok_kodu
