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
from .models import MusteriKayit,Sac,Boya, Yatak, MotorReduktor, Profil, Isleme, TeknolojikAlim,Log
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import MusteriKayitForm,SacForm,BoyaForm,YatakForm,MotorForm,ProfilForm,IslemeForm,TeknolojiForm
from django.db.models import Sum


def fetch_consolidated_data(request):
    data = []
    models = [
        (MusteriKayit, 'MusteriKayit'),
        (Sac, 'Sac'),
        (Boya, 'Boya'),
        (Yatak, 'Yatak'),
        (MotorReduktor, 'MotorReduktor'),
        (Profil, 'Profil'),
        (Isleme, 'Isleme'),
        (TeknolojikAlim, 'TeknolojikAlim')
    ]
    
    for model, table_name in models:
        try:
            # Dinamik olarak mevcut alanları kontrol et
            fields = model._meta.get_fields()
            field_names = [field.name for field in fields]
            
            if 'projekodu' in field_names:  # ForeignKey'nin `projekodu` ile alındığını varsayıyoruz
                # Veri çekme işlemi
                columns = [
                    'depo_secimi' if 'depo_secimi' in field_names else None,
                    'projekodu' if 'projekodu' in field_names else None,
                    'stok_kodu' if 'stok_kodu' in field_names else None,
                    'musteri' if 'musteri' in field_names else None
                ]
                columns = [col for col in columns if col is not None]  # None olanları kaldır

                # İlişkili projelerle veri çekme
                table_data = model.objects.all().select_related('projekodu').values(*columns)

                for item in table_data:
                    clean_item = {
                        'depo_secimi':item.get('depo_secimi', 'N/A'), 
                        'proje_kodu': item.get('projekodu', 'N/A'),  # ForeignKey'den veri çekiyoruz
                        'stok_kodu': item.get('stok_kodu', 'N/A'),
                        'musteri': item.get('musteri', 'N/A'),
                    }
                    data.append(clean_item)
                    print(clean_item)
                    
        except Exception as model_err:
            print(f"Error fetching data from {table_name}: {model_err}")
            continue
    
    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def index(request):
    
    context = {'segment': 'index'}
   

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))




    


  
@csrf_exempt
def musteri_kayit_ajax(request):
    if request.method == 'POST':
        form = MusteriKayitForm(request.POST)
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

#def search_stok_kodu(request):
#    query = request.GET.get('query', '')
#    results = list(Sac.objects.filter(stok_kodu__startswith=query).values('stok_kodu', 'projekodu__proje_kodu', 'musteri'))
#    print(results)
#    return JsonResponse({'results': results})
@csrf_exempt
def search_stok_kodu(request):
    query = request.GET.get('query', '')
    
    results = []

    models = [
        (Sac, 'Sac'),
        (Boya, 'Boya'),
        (Yatak, 'Yatak'),
        (MotorReduktor, 'MotorReduktor'),
        (Profil, 'Profil'),
        (Isleme, 'Isleme'),
        (TeknolojikAlim, 'TeknolojikAlim')
    ]
    
    for model, table_name in models:
        model_results = model.objects.filter(stok_kodu__startswith=query).values('stok_kodu', 'projekodu__proje_kodu', 'musteri', 'adet', 'id','depo_secimi')
        for result in model_results:
            result['table'] = table_name
        results.extend(model_results)

    return JsonResponse({'results': results})

@csrf_exempt
def update_stock(request):
    if request.method == 'POST':
        print(request.POST)
        # Formdan veri al
        stok_kodu = request.POST.get('stok_kodu')
        son_edit_tarih = request.POST.get('son_edit_tarih')
        cikis_aciklama = request.POST.get('cikis_aciklama')
        cikis_adeti = int(request.POST.get('cikis_adeti'))
        tablo = request.POST.get('tablo')

        # Tablo seçimine göre uygun modeli seç
        model_map = {
            'Sac': Sac,
            'Boya': Boya,
            'Yatak': Yatak,
            'MotorReduktor': MotorReduktor,
            'Profil': Profil,
            'Isleme': Isleme,
            'TeknolojikAlim': TeknolojikAlim,
        }

        if tablo in model_map:
            model = model_map[tablo]
            try:
                # Stok kodunu bul
                instance = model.objects.get(stok_kodu=stok_kodu)
                
                # Adet değerinden çıkış adedini düş
                if instance.adet >= cikis_adeti:
                    instance.adet -= cikis_adeti
                    instance.son_edit_tarih = son_edit_tarih
                    instance.updated_by =  request.user
                    instance.save()
                    return JsonResponse({'status': 'success', 'message': 'Stok güncellendi!'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'Yetersiz stok!'})

            except model.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Stok kodu bulunamadı!'})

        return JsonResponse({'status': 'error', 'message': 'Geçersiz tablo adı!'})

    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek!'})


    
@csrf_exempt
@login_required(login_url="/login/")
def depo_actions(request):
    try:

        # Veri setlerini alın, select_related kullanarak foreign key ile ilişkili verileri de yükleyin
        sac_data = list(Sac.objects.select_related('projekodu').all().values(
            'musteri',
            'projekodu',
            'stok_kodu',
            'adet',
            'depo_secimi',
            'olusturma_tarih',
            'son_edit_tarih',
            'giris_aciklama',
            'cikis_aciklama'
        ))
        boya_data = list(Boya.objects.select_related('projekodu').all().values(
            'musteri',
            'projekodu',
            'stok_kodu',
            'adet',
            'depo_secimi',
            'olusturma_tarih',
            'son_edit_tarih',
            'giris_aciklama',
            'cikis_aciklama'
        ))
        yatak_data = list(Yatak.objects.select_related('projekodu').all().values(
            'musteri',
            'projekodu',
            'stok_kodu',
            'adet',
            'depo_secimi',
            'olusturma_tarih',
            'son_edit_tarih',
            'giris_aciklama',
            'cikis_aciklama'
        ))
        profil_data = list(Profil.objects.select_related('projekodu').all().values(
            'musteri',
            'projekodu',
            'stok_kodu',
            'adet',
            'depo_secimi',
            'olusturma_tarih',
            'son_edit_tarih',
            'giris_aciklama',
            'cikis_aciklama'
        ))
        isleme_data = list(Isleme.objects.select_related('projekodu').all().values(
            'musteri',
            'projekodu',
            'stok_kodu',
            'adet',
            'depo_secimi',
            'olusturma_tarih',
            'son_edit_tarih',
            'giris_aciklama',
            'cikis_aciklama'
        ))
        motor_data = list(MotorReduktor.objects.select_related('projekodu').all().values(
            'musteri',
            'projekodu',
            'stok_kodu',
            'adet',
            'depo_secimi',
            'olusturma_tarih',
            'son_edit_tarih',
            'giris_aciklama',
            'cikis_aciklama'
        ))
        teknoloji_data = list(TeknolojikAlim.objects.select_related('projekodu').all().values(
            'musteri',
            'projekodu',
            'stok_kodu',
            'adet',
            'depo_secimi',
            'olusturma_tarih',
            'son_edit_tarih',
            'giris_aciklama',
            'cikis_aciklama'
        ))

        # Veri olup olmadığını kontrol et
        context = {
            'Sac': sac_data if sac_data else "Veri yok",
            'Boya': boya_data if boya_data else "Veri yok",
            'Yatak': yatak_data if yatak_data else "Veri yok",
            'Profil': profil_data if profil_data else "Veri yok",
            'Isleme': isleme_data if isleme_data else "Veri yok",
            'Motor': motor_data if motor_data else "Veri yok",
            'Teknoloji': teknoloji_data if teknoloji_data else "Veri yok"
        }

        html_template = loader.get_template('home/stok-action.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")

def get_chart_data_action(request):
    sac_count = Sac.objects.count()
    boya_count = Boya.objects.count()
    yatak_count = Yatak.objects.count()
    motor_count = MotorReduktor.objects.count()
    profil_count = Profil.objects.count()
    isleme_count = Isleme.objects.count()
    teknolojik_alim_count = TeknolojikAlim.objects.count()

    data = {
        'labels': [
            "Sac Deposu", 
            "Boya Deposu", 
            "Yatak Deposu", 
            "Motor Deposu", 
            "Profil Deposu", 
            "Isleme Deposu", 
            "Teknolojik Alım Deposu"
        ],
        'data': [
            sac_count, 
            boya_count, 
            yatak_count, 
            motor_count, 
            profil_count, 
            isleme_count, 
            teknolojik_alim_count
        ]
    }
    
    return JsonResponse(data)

def get_totals_chart_data(request):
    sac_total = Sac.objects.aggregate(total_adet=Sum('adet'))['total_adet'] or 0
    boya_total = Boya.objects.aggregate(total_adet=Sum('adet'))['total_adet'] or 0
    yatak_total = Yatak.objects.aggregate(total_adet=Sum('adet'))['total_adet'] or 0
    motor_total = MotorReduktor.objects.aggregate(total_adet=Sum('adet'))['total_adet'] or 0
    profil_total = Profil.objects.aggregate(total_adet=Sum('adet'))['total_adet'] or 0
    isleme_total = Isleme.objects.aggregate(total_adet=Sum('adet'))['total_adet'] or 0
    teknolojik_alim_total = TeknolojikAlim.objects.aggregate(total_adet=Sum('adet'))['total_adet'] or 0

    data = {
        'labels': [
            "Sac", 
            "Boya", 
            "Yatak", 
            "Motor Redüktör", 
            "Profil", 
            "İşleme", 
            "Teknolojik Alım"
        ],
        'data': [
            sac_total, 
            boya_total, 
            yatak_total, 
            motor_total, 
            profil_total, 
            isleme_total, 
            teknolojik_alim_total
        ]
    }
    
    return JsonResponse(data)

@csrf_exempt
@login_required(login_url="/login/")
def logshow(request):
       
    context = {'segment': 'index'}
  
   
    html_template = loader.get_template('home/action-logs.html')
    return HttpResponse(html_template.render(context, request,))

@csrf_exempt
@login_required(login_url="/login/")
def fetch_log_data(request):
  data = list(Log.objects.select_related('id').all().values(
    'action',
    'table_name',
    'username',
    'timestamp'
    ))

  return JsonResponse(data, safe=False)



from .tables import SacTable, BoyaTable, YatakTable, MotorReduktorTable, ProfilTable, IslemeTable, TeknolojikAlimTable

def sac_list(request):
    table = SacTable(Sac.objects.all())
    return render(request, 'home/sac_list.html', {'table': table})

def boya_list(request):
    table = BoyaTable(Boya.objects.all())
    return render(request, 'home/boya_list.html', {'table': table})

def yatak_list(request):
    table = YatakTable(Yatak.objects.all())
    return render(request, 'home/yatak_list.html', {'table': table})

def motor_reduktor_list(request):
    table = MotorReduktorTable(MotorReduktor.objects.all())
    return render(request, 'home/motor_reduktor_list.html', {'table': table})

def profil_list(request):
    table = ProfilTable(Profil.objects.all())
    return render(request, 'home/profil_list.html', {'table': table})

def isleme_list(request):
    table = IslemeTable(Isleme.objects.all())
    return render(request, 'home/isleme_list.html', {'table': table})

def teknolojik_alim_list(request):
    table = TeknolojikAlimTable(TeknolojikAlim.objects.all())
    return render(request, 'home/teknolojik_alim_list.html', {'table': table})