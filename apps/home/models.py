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
    musteri_kodu = models.CharField(max_length=255)
    adres = models.TextField()
    telefon = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        unique_together = ('musteri_adi', 'musteri_id', 'musteri_kodu')

    def __str__(self):
        return self.musteri_adi



class DepoGiris(models.Model):
    # Depo Giriş sayfası için uygun alanları belirleyin
    urun_kodu = models.CharField(max_length=255)
    urun_adi = models.CharField(max_length=255)
    miktar = models.IntegerField()
    tarih = models.DateTimeField()
    depo_adi = models.CharField(max_length=255)

    def __str__(self):
        return self.urun_adi

class DepoHareketleri(models.Model):
    hareket_sirasi = models.CharField(max_length=255)
    kullanici_kodu = models.CharField(max_length=255)
    tarih = models.DateTimeField()
    hangi_depo = models.CharField(max_length=255)
    stok_kodu = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.hareket_sirasi} - {self.kullanici_kodu}"

class Sac(models.Model):
    musteri = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE)
    stok_kodu = models.CharField(max_length=255)
    proje = models.CharField(max_length=255)
    kalinlik = models.DecimalField(max_digits=10, decimal_places=2)
    boy = models.DecimalField(max_digits=10, decimal_places=2)
    adet = models.IntegerField()
    kalite = models.CharField(max_length=255)
    depo_secimi = models.CharField(max_length=255)
    tarih = models.DateTimeField()

    def __str__(self):
        return self.stok_kodu

    

class Profil(models.Model):
    musteri = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE)
    stok_kodu = models.CharField(max_length=255)
    proje = models.CharField(max_length=255)
    kalinlik = models.DecimalField(max_digits=10, decimal_places=2)
    boy = models.DecimalField(max_digits=10, decimal_places=2)
    adet = models.IntegerField()
    kalite = models.CharField(max_length=255)
    depo_secimi = models.CharField(max_length=255)
    tarih = models.DateTimeField()

    def __str__(self):
        return self.stok_kodu



class Boya(models.Model):
    musteri = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE)
    stok_kodu = models.CharField(max_length=255)
    proje = models.CharField(max_length=255)
    renk = models.CharField(max_length=255)
    miktar = models.DecimalField(max_digits=10, decimal_places=2)
    depo_secimi = models.CharField(max_length=255)
    tarih = models.DateTimeField()

    def __str__(self):
        return self.stok_kodu

    
class MotorReduktor(models.Model):
    musteri = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE)
    stok_kodu = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    guc = models.DecimalField(max_digits=10, decimal_places=2)
    adet = models.IntegerField()
    depo_secimi = models.CharField(max_length=255)
    tarih = models.DateTimeField()

    def __str__(self):
        return self.stok_kodu


class MotorReduktor(models.Model):
    musteri = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE)
    stok_kodu = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    guc = models.DecimalField(max_digits=10, decimal_places=2)
    adet = models.IntegerField()
    depo_secimi = models.CharField(max_length=255)
    tarih = models.DateTimeField()

    def __str__(self):
        return self.stok_kodu


class Isleme(models.Model):
    musteri = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE)
    stok_kodu = models.CharField(max_length=255)
    islem_tipi = models.CharField(max_length=255)
    miktar = models.DecimalField(max_digits=10, decimal_places=2)
    depo_secimi = models.CharField(max_length=255)
    tarih = models.DateTimeField()

    def __str__(self):
        return self.stok_kodu


class TeknolojikAlim(models.Model):
    musteri = models.ForeignKey(MusteriKayit, on_delete=models.CASCADE)
    stok_kodu = models.CharField(max_length=255)
    malzeme_tipi = models.CharField(max_length=255)
    miktar = models.DecimalField(max_digits=10, decimal_places=2)
    depo_secimi = models.CharField(max_length=255)
    tarih = models.DateTimeField()

    def __str__(self):
        return self.stok_kodu




