# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Sac
from .models import MusteriKayit, DepoHareket, Sac, Profil, Boya, MotorReduktor, Isleme
#TeknolojikAlim
#
## Register your models here.
#admin.site.register(MusteriKayit)
#admin.site.register(DepoHareket)
admin.site.register(Sac)
admin.site.register(Profil)
admin.site.register(Boya)
admin.site.register(MotorReduktor)
admin.site.register(Isleme)
#admin.site.register(TeknolojikAlim)