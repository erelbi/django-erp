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
from .forms import MusteriKayitForm,SacForm,BoyaForm,YatakForm,MotorForm,ProfilForm,IslemeForm,TeknolojiForm


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))




    


  
@csrf_exempt
def musteri_kayit_ajax(request):
    if request.method == 'POST':
        form = MusteriKayitForm(request.POST)
        print(form)
        proje_kodu = request.POST.get('proje_kodu')
        if MusteriKayit.objects.filter(proje_kodu=proje_kodu).exists():
            return JsonResponse({'success': False, 'message': ' Proje kodu benzersiz olmalıdır.'})
        if form.is_valid():
            try:
                musteri_kayit = form.save(commit=False)
                musteri_kayit.created_by = request.user
                musteri_kayit.save()
                form.save()
                return JsonResponse({'success': True, 'message': 'Müşteri başarıyla kaydedildi.'})
            except IntegrityError:
                return JsonResponse({'success': False, 'message': ' Proje kodu benzersiz olmalıdır.'})
        else:
            print(form.errors)
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

@csrf_exempt
@login_required(login_url="/login/")
def mkd(request):
    if request.method == 'POST':
        cell_value = request.POST['cellId']
        musteri_id = request.POST['musteri_id']
        new_value = request.POST['value']
        if cell_value == "proje_kodu":
            if MusteriKayit.objects.filter(proje_kodu=new_value).exists():
                return JsonResponse({'success': False, 'message': ' Proje kodu benzersiz olmalıdır.'})
        try:
            musteri_kayit = MusteriKayit.objects.get(musteri_id=musteri_id)
            setattr(musteri_kayit, cell_value, new_value)
            setattr(musteri_kayit, 'updated_by', request.user)
            musteri_kayit.save()
            return JsonResponse({'success': True, 'message': 'Müşteri başarıyla düzenlendi.'})
        except Exception as err:
            return JsonResponse({'success': False, 'message': 'HATA : {}'.format(err)})

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


@csrf_exempt
@login_required(login_url="/login/")
def stokimport(request):
    try:
        proje_kodlari = MusteriKayit.objects.values_list('proje_kodu', flat=True)
        musteri_adlari = MusteriKayit.objects.values_list('musteri_adi', flat=True)
        context = {'segment': 'depo giriş','proje_kodlari':proje_kodlari,'musteri_adlari':musteri_adlari}
        html_template = loader.get_template('home/stok-import.html')
        
        return HttpResponse(html_template.render(context, request))
    except Exception as err:
        print(err)
        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(request))

@csrf_exempt
def sac_kayit_ajax(request):
    if request.method == 'POST':
        form = SacForm(request.POST)
        if form.is_valid():
            try:
                sac_kayit = form.save(commit=False)
                sac_kayit.created_by = request.user
                sac_kayit.projekodu = form.cleaned_data['projekodu']
                sac_kayit.save()
                return JsonResponse({'success': True, 'message': 'Kayıt İşlemi Başarılı.Stok Kodu: ', 'stok_kodu': sac_kayit.stok_kodu})
            except MusteriKayit.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Belirtilen proje kodu bulunamadı.'})
            except Exception as err:
                return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {err}'})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'message': 'Form geçersiz. Lütfen tüm alanları doğru doldurun.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})


@csrf_exempt
def boya_kayit_ajax(request):
    if request.method == 'POST':
        form = BoyaForm(request.POST)
        if form.is_valid():
            try:
                boya_kayit = form.save(commit=False)
                boya_kayit.created_by = request.user
                boya_kayit.projekodu = form.cleaned_data['projekodu'] 
                boya_kayit.save()
                return JsonResponse({'success': True, 'message': 'Kayıt İşlemi Başarılı.Stok Kodu: ', 'stok_kodu': boya_kayit.stok_kodu})
            except MusteriKayit.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Belirtilen proje kodu bulunamadı.'})
            except Exception as err:
                return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {err}'})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'message': 'Form geçersiz. Lütfen tüm alanları doğru doldurun.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})


@csrf_exempt
def yatak_kayit_ajax(request):
    if request.method == 'POST':
        form = YatakForm(request.POST)
        if form.is_valid():
            try:
                yatak_kayit = form.save(commit=False)
                yatak_kayit.created_by = request.user
                yatak_kayit.projekodu = form.cleaned_data['projekodu'] 
                yatak_kayit.save()
                return JsonResponse({'success': True, 'message': 'Kayıt İşlemi Başarılı.Stok Kodu: ', 'stok_kodu': yatak_kayit.stok_kodu})
            except MusteriKayit.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Belirtilen proje kodu bulunamadı.'})
            except Exception as err:
                return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {err}'})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'message': 'Form geçersiz. Lütfen tüm alanları doğru doldurun.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})


@csrf_exempt
def motor_kayit_ajax(request):
    if request.method == 'POST':
        form = MotorForm(request.POST)
        if form.is_valid():
            try:
                motor_kayit = form.save(commit=False)
                motor_kayit.created_by = request.user
                motor_kayit.projekodu = form.cleaned_data['projekodu'] 
                motor_kayit.save()
                return JsonResponse({'success': True, 'message': 'Kayıt İşlemi Başarılı.Stok Kodu: ', 'stok_kodu': motor_kayit.stok_kodu})
            except MusteriKayit.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Belirtilen proje kodu bulunamadı.'})
            except Exception as err:
                return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {err}'})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'message': 'Form geçersiz. Lütfen tüm alanları doğru doldurun.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})


@csrf_exempt
def profil_kayit_ajax(request):
    if request.method == 'POST':
        form = ProfilForm(request.POST)
        print(form.data)
        if form.is_valid():
            try:
                profil_kayit = form.save(commit=False)
                profil_kayit.created_by = request.user
                profil_kayit.projekodu = form.cleaned_data['projekodu']
                profil_kayit.save()
                return JsonResponse({'success': True, 'message': 'Kayıt İşlemi Başarılı.Stok Kodu: ', 'stok_kodu': profil_kayit.stok_kodu})
            except MusteriKayit.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Belirtilen proje kodu bulunamadı.'})
            except Exception as err:
                return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {err}'})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'message': 'Form geçersiz. Lütfen tüm alanları doğru doldurun.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})

@csrf_exempt
def isleme_kayit_ajax(request):
    if request.method == 'POST':
        form = IslemeForm(request.POST)
        #print(form.data)
        if form.is_valid():
            try:
                isleme_kayit = form.save(commit=False)
                isleme_kayit.created_by = request.user
                isleme_kayit.projekodu = form.cleaned_data['projekodu']
                isleme_kayit.save()
                return JsonResponse({'success': True, 'message': 'Kayıt İşlemi Başarılı.Stok Kodu: ', 'stok_kodu': isleme_kayit.stok_kodu})
            except MusteriKayit.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Belirtilen proje kodu bulunamadı.'})
            except Exception as err:
                return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {err}'})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'message': 'Form geçersiz. Lütfen tüm alanları doğru doldurun.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})

@csrf_exempt
def isleme_kayit_ajax(request):
    if request.method == 'POST':
        form = TeknolojiForm(request.POST)
        #print(form.data)
        if form.is_valid():
            try:
                isleme_kayit = form.save(commit=False)
                isleme_kayit.created_by = request.user
                isleme_kayit.projekodu = form.cleaned_data['projekodu']
                isleme_kayit.save()
                return JsonResponse({'success': True, 'message': 'Kayıt İşlemi Başarılı.Stok Kodu: ', 'stok_kodu': isleme_kayit.stok_kodu})
            except MusteriKayit.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Belirtilen proje kodu bulunamadı.'})
            except Exception as err:
                return JsonResponse({'success': False, 'message': f'Bir hata oluştu: {err}'})
        else:
            print(form.errors)
            return JsonResponse({'success': False, 'message': 'Form geçersiz. Lütfen tüm alanları doğru doldurun.'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})