# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('musteri-kayit-olustur', views.mko, name='mko'),
    path('musteri-kayit-duzenle', views.mkd, name='musteri_kaydi_duzenle'),
    path('musteri-kayit-sil', views.mks, name='mks'),
    path('musteri-kayit-ajax', views.musteri_kayit_ajax, name='musteri_kayit_ajax'),
    path('musteri-liste/', views.musteri_liste, name='musteri_liste'),
    path('depo_giris', views.stokimport, name='depo_giris'),
    path('sac-kayit-ajax', views.sac_kayit_ajax, name='sac_kayit_ajax'),
    path('boya-kayit-ajax', views.boya_kayit_ajax, name='boya_kayit_ajax'),
    path('yatak-kayit-ajax', views.yatak_kayit_ajax, name='yatak_kayit_ajax'),
    path('motor-kayit-ajax', views.motor_kayit_ajax, name='motor_kayit_ajax'),
    path('profil-kayit-ajax', views.profil_kayit_ajax, name='profil_kayit_ajax'),
    path('isleme-kayit-ajax', views.isleme_kayit_ajax, name='isleme_kayit_ajax'),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
