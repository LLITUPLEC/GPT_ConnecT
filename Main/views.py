# -*- coding: utf-8 -*-
from datetime import datetime
from pprint import pprint

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from BS.models import Bs_depowner, Bs_department, Bs_RWway
from KMO.models import Kmo, Kmo_members, Kmodet, Kmo_responsible
from KMO.forms import Kmo_membersFormSet, KMOForm_edit, KMO_check_create, KMOdetForm_edit, KMOdetForm_create
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse, JsonResponse
from django.contrib import messages
from qrgenerator.forms import QR_create

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from Main.models import Profile
from qrcode import make as make_qr

from qrgenerator.models import Bar_code

pdfmetrics.registerFont(TTFont('DejaVuSerif', 'static/DejaVuSerif.ttf', 'UTF-8'))


def index(request):
    return render(request, 'Main/index.html')


@login_required
def kmo(request):
    bs_deps = Bs_depowner.objects.all()
    list_kmo = Kmo.objects.all()

    error = ''
    if request.method == 'POST':

        check_form_kmo = KMO_check_create(request.POST)

        if check_form_kmo.is_valid():
            validate = check_form_kmo.check_kmo_date_and_dep()
            if validate == 'error_date_dep':
                messages.info(request, 'Создание невозможно! КМО в указанном периоде и филиале уже существует')
                return HttpResponseRedirect('/kmo')
            else:
                check_form_kmo.instance.user_creator = request.user.username
                check_form_kmo.instance.idprofile = Profile.objects.filter(chairman=True, iddepowner=check_form_kmo.instance.iddepowner).first()
                id_dorm = check_form_kmo.save()

            return redirect(f'edit_kmo/{id_dorm.id}')
        else:
            error = 'Форма ошибочна \n' + str(check_form_kmo.errors)
    else:
        current_datetime = datetime.now()
        created_at__year = str(current_datetime.year)
        created_at__month = str(current_datetime.month)
        created_at__hour = str(current_datetime.hour)
        s_dep_first_letter = Profile.objects.filter(user=request.user).values('iddepartment').first()
        kmo = Kmo(n_regnumber=created_at__month + '/' + created_at__year + '-' + created_at__hour + '_' + str(
            s_dep_first_letter['iddepartment'], ),
                  date_detection=current_datetime.date())
        check_form_kmo = KMO_check_create(instance=kmo)

    return render(request, 'KMO/index.html',
                  {'title_view': 'Список КМО!', 'deps': bs_deps, 'all_kmo': list_kmo, 'check_form_kmo': check_form_kmo})


def about(request):
    return render(request, 'Main/about.html')


@login_required
def bs(request):
    all_bs_models = ['Филиалы', 'Подразделения', 'Должности', 'ЖД Станции']
    return render(request, 'BS/index.html', {'title_view': 'Список справочников!', 'bss': all_bs_models})


# @login_required
# def check_create_kmo(request):
#
#     # if request.user.groups.filter(name='worker_view').count():
#         print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW')
#         error = ''
#         if request.method == 'POST':
#
#             check_form_kmo = KMO_check_create(request.POST)
#
#             if check_form_kmo.is_valid():
#
#                 check_form_kmo.instance.user_creator = request.user.username
#                 check_form_kmo.save()
#                 return redirect('kmo')
#             else:
#                 error = 'Форма ошибочна \n' + str(check_form_kmo.errors)
#         else:
#             try:
#                 list_kmo_id = Kmo.objects.last().id
#             except:
#                 list_kmo_id = '1'
#             kmo = Kmo(n_regnumber=list_kmo_id)
#             check_form_kmo = KMOForm(instance=kmo)
#             context = {
#                 'title_view': 'Создать Акт КМО',
#                 'check_form_kmo': check_form_kmo,
#                 'error': error,
#             }
#             return render(request, 'KMO/create_kmo.html', context)
#     # else:
#     #     messages.info(request, 'Ваших прав недостаточно! Обратитесь к администратору')
#     #     return HttpResponseRedirect('/kmo')




@login_required()
def delete(request, kmo_id):
    if request.user.groups.filter(name='delete_kmo').count():
        kmo = get_object_or_404(Kmo, id=kmo_id)
        kmo.delete()
        return redirect('/kmo')
    else:
        messages.info(request, 'Ваших прав недостаточно! Обратитесь к администратору')
        return HttpResponseRedirect('/kmo')

@login_required()
def delete_members(request, form_h_id):
    # if request.user.groups.filter(name='worker_view').count():
    members = get_object_or_404(Kmo_members, id=form_h_id)
    members.delete()
    # return (request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# else:
#     messages.info(request, 'Ваших прав недостаточно! Обратитесь к администратору')
#     return HttpResponseRedirect('/kmo')
@login_required()
def edit_kmo(request, kmo_id):
    kmo = get_object_or_404(Kmo, id=kmo_id)
    if kmo.approved:
        return redirect(f'/view_kmo/{kmo_id}')
    if request.method == 'POST':
        # print('}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}11111111111111111')
        edit_form = KMOForm_edit(request.POST, instance=kmo)
        # for field in edit_form:
        #     print("Field Error:", 'field.name => ', field.name, 'field.errors => ', field.errors)
        # print('1) }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}edit_form.instance.id ', edit_form.instance.id)
        # print('2) }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}edit_form.instance.created_at ', edit_form.instance.created_at)
        # print('3) }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}edit_form.instance.user_creator ', edit_form.instance.user_creator)
        # print('4) }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}edit_form.instance.s_update_user ', edit_form.instance.s_update_user)
        # print('5) }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}edit_form.instance.updated_at ', edit_form.instance.updated_at)
        # print('6) }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}edit_form.instance.n_regnumber ', edit_form.instance.n_regnumber)
        # print('7) }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}edit_form.instance.date_detection ', edit_form.instance.date_detection)
        # print('8) }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}edit_form.instance.idprofile ', edit_form.instance.idprofile)
        # print('8) }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}edit_form.instance.idprofile ', edit_form.instance.iddepowner)
        form_members = Kmo_membersFormSet(request.POST)
        # print('}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}33333333333333333', 'edit_form.is_bound => ', edit_form.is_bound)
        # print('}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}44444444', 'edit_form.is_valid() => ', edit_form.is_valid())
        if edit_form.is_valid() and form_members.is_valid():
            edit_form.instance.s_update_user = request.user.username
            edit_form.save()
            form_members.save()
            print(
                '_______________________________________________SSSSSSSSAAAAAAAAAAAAAAAAVVVVVVVVVVVVEEEEEEEEEEE_______________________')
            # return redirect('edit_kmo', edit_form.instance.id)
            return redirect('kmo')
    else:
        edit_form = KMOForm_edit(instance=kmo)
        form_members = Kmo_members.objects.filter(idkmo=kmo_id)
        kmo_data = Kmo.objects.get(id=kmo_id)
        form_add_members = Kmo_membersFormSet(queryset=Kmo_members.objects.none())

        data_kmodet_sp = Kmodet.objects.filter(idkmo=kmo_id, iddepartment=Bs_department.objects.get(s_name='СП'))
        data_kmodet_scb = Kmodet.objects.filter(idkmo=kmo_id, iddepartment=Bs_department.objects.get(s_name='СЦБ'))
        data_kmodet_count_all = Kmodet.objects.filter(idkmo=kmo_id).count()
        data_kmodet_count_overdue = Kmodet.objects.filter(idkmo=kmo_id, date_elimination__lt=datetime.now().date(),
                                                          eliminated=0).count()
        data_kmodet_count_active = Kmodet.objects.filter(idkmo=kmo_id, eliminated=0).count()
        content = {'title_view': 'Редактирование',
                   'edit_form': edit_form,
                   'kmo_data': kmo_data,
                   'form_members': form_members,
                   'form_add_members': form_add_members,
                   'id_kmo_edit': kmo_id,
                   'data_kmodet_sp': data_kmodet_sp,
                   'data_kmodet_scb': data_kmodet_scb,
                   'data_kmodet_all': {
                       'kmodet_all_count': data_kmodet_count_all,
                       'kmodet_count_overdue': data_kmodet_count_overdue,
                       'kmodet_count_active': data_kmodet_count_active,
                       'datenow': datetime.now().date()
                   }
                   }

        return render(request, 'KMO/edit_kmo.html', context=content)


@login_required()
def view_kmo(request, kmo_id):
    kmo = get_object_or_404(Kmo, id=kmo_id)
    view_form = KMOForm_edit(instance=kmo)
    form_members = Kmo_members.objects.filter(idkmo=kmo_id)
    kmo_data = Kmo.objects.get(id=kmo_id)
    data_kmodet_sp = Kmodet.objects.filter(idkmo=kmo_id, iddepartment=Bs_department.objects.get(s_name='СП'))
    data_kmodet_scb = Kmodet.objects.filter(idkmo=kmo_id, iddepartment=Bs_department.objects.get(s_name='СЦБ'))
    data_kmodet_count_all = Kmodet.objects.filter(idkmo=kmo_id).count()
    data_kmodet_count_overdue = Kmodet.objects.filter(idkmo=kmo_id, date_elimination__lt=datetime.now().date(),
                                                      eliminated=0).count()
    data_kmodet_count_active = Kmodet.objects.filter(idkmo=kmo_id, eliminated=0).count()

    content = {'title_view': 'Просмотр КМО',
               # 'view_form': view_form,
               'view_form': kmo,
               'kmo_data': kmo_data,
               'form_members': form_members,
               'id_kmo_edit': kmo_id,
               'data_kmodet_sp': data_kmodet_sp,
               'data_kmodet_scb': data_kmodet_scb,
               'data_kmodet_all': {
                   'kmodet_all_count': data_kmodet_count_all,
                   'kmodet_count_overdue': data_kmodet_count_overdue,
                   'kmodet_count_active': data_kmodet_count_active,
                   'datenow': datetime.now().date()
               }
               }

    return render(request, 'KMO/view_kmo.html', context=content)


@login_required()
def approv_kmo(request, kmo_id):
    kmo = get_object_or_404(Kmo, id=kmo_id)
    if kmo.idprofile and request.user == kmo.idprofile.user:
        kmo.approved = 1
        kmo.save()
        return redirect(f'/view_kmo/{kmo_id}')
    else:
        dop_msg = '! А он даже не указан' if not kmo.idprofile else ''
        messages.info(request, 'Утверждение невозможно! Только председатель данного КМО имеет на это право' + dop_msg)
        return HttpResponseRedirect(f'/edit_kmo/{kmo_id}')


    # return render(request, 'KMO/view_kmo.html')

def kmo_pdf(request, kmo_id):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    texob = c.beginText()
    texob.setTextOrigin(25, 100)
    texob.setFont("DejaVuSerif", 14)
    kmo_obj = get_object_or_404(Kmo, id=kmo_id)

    texob.textLine("Создатель документа: " + kmo_obj.user_creator)
    texob.textLine("Рег. номер: " + str(kmo_obj.n_regnumber))
    texob.textLine("Дата обнаружения: " + str(kmo_obj.date_detection))
    # texob.textLine("Станция: " + str(kmo_obj.idRWStation))
    # texob.textLine("Срок устранения: " + str(kmo_obj.date_elimination))

    c.drawText(texob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='test_try.pdf')


#  ПОЗИЦИИ КМО ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@login_required()
def delete_kmo_det(request, kmodet_id):
    if request.user.groups.filter(name='delete_kmodet').count():
        kmodet = get_object_or_404(Kmodet, id=kmodet_id)
        if kmodet.idkmo.approved:
            messages.info(request, 'Удаление невозможно, КМО утверждён председателем!')
            return HttpResponseRedirect(f'/view_kmo/{kmodet.idkmo.pk}')
        kmodet.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    else:
        messages.info(request, 'Ваших прав недостаточно! Обратитесь к администратору')
        return HttpResponseRedirect('/kmo')


@login_required()
def create_kmo_det(request, kmo_id, kmo_det_department):
    # if request.user.groups.filter(name='worker_view').count():
    idKMO = Kmo.objects.get(id=kmo_id)
    if idKMO.approved:
        return HttpResponseRedirect(f'/view_kmo/{kmo_id}')
    error = ''
    if request.method == 'POST':
        print('=========== POST =============')
        form_create_kmodet = KMOdetForm_edit(request.POST, request.FILES)
        if form_create_kmodet.is_valid():
            print('=========== form_create_kmodet is_valid=============')
            form_create_kmodet.instance.user_creator = request.user.username
            form_create_kmodet.save()
            # return render(request, 'KMO/index.html')
            return redirect(f'/edit_kmo/{kmo_id}')
        else:
            error = 'Форма ошибочна \n' + str(form_create_kmodet.errors)
    else:
        idDepartment = Bs_department.objects.get(id=kmo_det_department)
        idDepowner_row = Kmo.objects.filter(id=kmo_id).values('iddepowner').first()
        idresponsible_f = Kmo_responsible.objects.filter(iddepowner=idKMO.iddepowner, iddepartment=idDepartment).first()
        idDepowner = Bs_depowner.objects.get(id=idDepowner_row['iddepowner'])
        kmodet = Kmodet(idkmo=idKMO, iddepartment=idDepartment, date_detection=datetime.now().date(),
                        user_creator=request.user.username, iddepowner=idDepowner, idresponsible=idresponsible_f)

        form_create_kmodet = KMOdetForm_create(instance=kmodet)

        context = {
            'title_view': 'Создать неисправность КМО',
            'form_create_kmodet': form_create_kmodet,
            'header_KMO_data': idKMO,
            'idDepartment': idDepartment,
            'error': error,
        }
        return render(request, 'KMO/KMO_det/create_kmo_det.html', context)


# else:
#     messages.info(request, 'Ваших прав недостаточно! Обратитесь к администратору')
#     return HttpResponseRedirect('/kmo')

@login_required()
def edit_kmo_det(request, kmodet_id):
    kmodet = get_object_or_404(Kmodet, id=kmodet_id)
    if kmodet.idkmo.approved:
        return HttpResponseRedirect(f'/view_kmo_det/{kmodet_id}')
    if request.method == 'POST':
        edit_form = KMOdetForm_create(request.POST, request.FILES, instance=kmodet)
        pprint(edit_form)
        if edit_form.is_valid():
            edit_form.instance.s_update_user = request.user.username
            edit_form.save()
            return redirect(f"/edit_kmo/{kmodet.idkmo.pk}")
    else:
        edit_kmodet_form = KMOdetForm_create(instance=kmodet)
        depart = edit_kmodet_form.instance.iddepartment
        header_KMO_data = Kmo.objects.get(id=kmodet.idkmo.pk)
        content = {'title_view': 'Редактирование неисправности',
                   'edit_kmodet_form': edit_kmodet_form,
                   # 'form_create_kmodet': edit_kmodet_form,
                   'header_KMO_data': header_KMO_data,
                   'iddepartment': depart,
                   'iddepowner_f': header_KMO_data.iddepowner,
                   }

        return render(request, 'KMO/KMO_det/edit_kmo_det.html', context=content)


def zadeploil(request):
    return render(request, 'Main/z.html')


@login_required()
def view_kmo_det(request, kmodet_id):
    kmodet = get_object_or_404(Kmodet, id=kmodet_id)
    kmo_main = Kmodet.objects.filter(id=kmodet_id).values('idkmo').first()
    depart = kmodet.iddepartment
    header_KMO_data = Kmo.objects.get(id=kmo_main['idkmo'])
    content = {'title_view': 'Редактирование неисправности',
               'view_kmodet': kmodet,
               'header_KMO_data': header_KMO_data,
               'iddepartment': depart,
               }

    return render(request, 'KMO/KMO_det/view_kmo_det.html', context=content)


@login_required()
def done_kmo_det(request, kmodet_id):
    # if request.user.groups.filter(name='worker_view').count():
    kmodet = get_object_or_404(Kmodet, id=kmodet_id)
    if kmodet.idkmo.approved is False:
        messages.info(request, 'ОШИБКА! Устранять неисправности можно только ПОСЛЕ утверждения КМО')
        return HttpResponseRedirect(f'/view_kmo/{kmodet.idkmo.pk}')
    if request.user == kmodet.idresponsible.idprofile.user:
        kmodet.eliminated = True
        kmodet.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.info(request, 'ОШИБКА! Признак устранения может ставить Пользователь, '
                               'указанный в графе "Ответственный за устранение"')
        return HttpResponseRedirect(f'/view_kmo/{kmodet.idkmo.pk}')


def index_qr(request):

    if request.method == "POST":
        QR_create_form = QR_create(request.POST)
        QR_create_form.instance.type_object = request.POST['type_object']
        if QR_create_form.is_valid():
            QR_create_form.instance.s_create_user = request.user.username
            QR_create_form.save()
            # return render(request, 'qrgenerator/index.html')
        else:
            error = 'Форма ошибочна \n' + str(QR_create_form.errors)
    else:
        # print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
        qr_code = Bar_code()
        QR_create_form = QR_create(instance=qr_code)

    return render(request, 'qrgenerator/index.html', {'qr_form': QR_create_form, 'qwe': 'qqqq'})


@login_required()
def view_kmodet_by_qr(request, type_obj, id_obj):
    if type_obj == 'stp':
        obj_rows = Kmodet.objects.filter(idrwsp=id_obj).order_by('date_detection').reverse()  # Если стрелочные переводы
        obj_row_last = Kmodet.objects.filter(idrwsp=id_obj).last()  # Если стрелочные переводы(последняя запись)
        name_obj = f'Стрелочный Перевод №{obj_row_last.idrwsp.s_name} ст.{obj_row_last.idrwsp.idrwstation.s_name}'
    elif type_obj == 'way':
        obj_rows = Kmodet.objects.filter(idrwway=id_obj)  # Если жд пути
        obj_row_last = Kmodet.objects.filter(idrwway=id_obj).last()  # Если стрелочные переводы(последняя запись)
    else:
        obj_row_last = 'None 1'
        obj_rows = 'None 2'

    return render(request, 'KMO/KMO_det/view_kmodet_by_qr.html', {'obj_row_last': obj_row_last,
                                                                  'obj_rows': obj_rows,
                                                                  'url_kmo': f'/view_kmo/{obj_row_last.idkmo.pk}',
                                                                  'name_obj': name_obj}
                  )


