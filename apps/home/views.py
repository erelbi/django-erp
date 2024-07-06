# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.http import JsonResponse
from django import template
from django import forms
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import MusteriKayit
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))




class MusteriKayitForm(forms.ModelForm):
    class Meta:
        model = MusteriKayit
        fields = ['musteri_adi', 'musteri_kodu', 'adres', 'telefon', 'email']


  
@csrf_exempt
def musteri_kayit_ajax(request):
    print(request)
    if request.method == 'POST':
        form = MusteriKayitForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'success': True, 'message': 'Müşteri başarıyla kaydedildi.'})
            except IntegrityError:
                return JsonResponse({'success': False, 'message': 'Müşteri adı, ID veya kodu benzersiz olmalıdır.'})
        else:
            return JsonResponse({'success': False, 'message': 'Form geçersiz. Lütfen tüm alanları doğru doldurun.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})

@login_required(login_url="/login/")
def mko(request):
    if request.method == 'POST':
        form = MusteriKayitForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Müşteri başarıyla kaydedildi.')
                #return redirect('musteri-kayit-olustur')  # Kayıt başarılı olduğunda yönlendirilecek sayfa
            except IntegrityError:
                messages.error(request, 'Müşteri adı, ID veya kodu benzersiz olmalıdır.')
                form.add_error(None, 'Müşteri adı, ID veya kodu benzersiz olmalıdır.')
    else:
        form = MusteriKayitForm()
    html_template = loader.get_template('home/kayit-olustur.html')
    context = {'segment': 'index','form':form}
    return HttpResponse(html_template.render(context, request))

    #html_template = loader.get_template('home/index.html')
    #


@login_required(login_url="/login/")
def mks(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def musteri_liste(request):
    musteriler = MusteriKayit.objects.all().values('id', 'musteri_adi', 'musteri_kodu', 'adres', 'telefon', 'email')
    data = list(musteriler)
    return JsonResponse({'data': data})

@login_required(login_url="/login/")
def mkd(request):
    musteriler = MusteriKayit.objects.all()
    data = list(musteriler)
    context = {'segment': 'index','data':data}
    html_template = loader.get_template('home/kayit-duzenle.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
