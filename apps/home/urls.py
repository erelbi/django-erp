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
    path('musteri-kayit-duzenle', views.mkd, name='mkd'),
    path('musteri-kayit-sil', views.mks, name='mks'),
    path('musteri-kayit-ajax', views.musteri_kayit_ajax, name='musteri_kayit_ajax'),
    path('musteri-liste/', views.musteri_liste, name='musteri_liste'),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
