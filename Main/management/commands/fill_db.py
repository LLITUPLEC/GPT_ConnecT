import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from BS.models import Bs_depowner, Bs_department, Bs_position, Bs_RWStation, Bs_Obj_insp, Bs_RW_element, \
    Bs_RW_defect_gr, Bs_RW_defect_tp, Bs_RWway
from main.models import Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create_superuser('tminn', 'tminn91@mail.ru', '123')

        # BEGIN_филиалы-------------------------------------------------------------------------------------------------
        depown_path = f"static/bs/Филиалы.xlsx"  # файл с указанием названий филиалов
        get_depown = pd.read_excel(depown_path)
        for idx_data in get_depown.index:
            depowner = Bs_depowner(s_mnemocode=get_depown['Мнемокод'][idx_data],
                                   s_name=get_depown['Название'][idx_data],
                                   s_create_user='auto_fill',
                                   not_used=False)
            depowner.save()
        # END_филиалы---------------------------------------------------------------------------------------------------

        # BEGIN_Подразделения-------------------------------------------------------------------------------------------
        depart_path = f"static/bs/Подразделения.xlsx"  # файл с указанием названий филиалов
        get_depart = pd.read_excel(depart_path)
        for idx_data in get_depart.index:
            department = Bs_department(s_mnemocode=get_depart['Мнемокод'][idx_data],
                                       s_name=get_depart['Название'][idx_data],
                                       s_create_user='auto_fill',
                                       part_kmo=get_depart['Участвует в КМО'][idx_data],
                                       not_used=False)
            department.save()
        # END_Подразделения---------------------------------------------------------------------------------------------

        # BEGIN_Должность-----------------------------------------------------------------------------------------------
        position_path = f"static/bs/Должности.xlsx"  # файл с указанием названий филиалов
        get_position = pd.read_excel(position_path)
        for idx_data in get_position.index:
            position = Bs_position(s_mnemocode=get_position['Мнемокод'][idx_data],
                                   s_name=get_position['Название'][idx_data],
                                   s_create_user='auto_fill',
                                   not_used=0)
            position.save()
        # END_Должность-------------------------------------------------------------------------------------------------

        # BEGIN_работники-----------------------------------------------------------------------------------------------
        worker_path = f"static/bs/Работники.xlsx"  # файл с указанием названий филиалов
        get_worker = pd.read_excel(worker_path)
        for idx_data in get_worker.index:
            User.objects.create_user(str(get_worker['Логин'][idx_data]),
                                     str(get_worker['Email'][idx_data]),
                                     str(get_worker['Пароль'][idx_data]))
            worker = Profile.objects.get(user=User.objects.get(username=get_worker['Логин'][idx_data]))
            worker.first_name = get_worker['Имя'][idx_data]
            worker.last_name = get_worker['Фамилия'][idx_data]
            worker.third_name = get_worker['Отчество'][idx_data]
            worker.iddepowner = Bs_depowner.objects.get(s_name=get_worker['Филиал'][idx_data])
            worker.iddepartment = Bs_department.objects.get(s_name=get_worker['Служба'][idx_data])
            worker.idposition = Bs_position.objects.get(s_name=get_worker['Должность'][idx_data])
            worker.d_birthday = get_worker['ДР'][idx_data]
            worker.d_hiring = get_worker['Дата приёма'][idx_data]
            worker.chairman = get_worker['яв-ся председателем'][idx_data]
            worker.member_kmo = get_worker['яв-ся членом комиссии'][idx_data]
            worker.s_create_user = 'auto_fill'
            worker.save()
        # END_работники-------------------------------------------------------------------------------------------------

        # BEGIN_ЖД станция/участок--------------------------------------------------------------------------------------
        data_path_stations = f"static/bs/Станции.xlsx"  # файл с указанием названий филиалов
        get_data_station = pd.read_excel(data_path_stations)
        for idx_data_station in get_data_station.index:
            rwStation = Bs_RWStation(s_mnemocode=get_data_station['Мнемокод'][idx_data_station],
                                     s_name=get_data_station['Название'][idx_data_station],
                                     s_create_user='auto_fill',
                                     iddepowner=Bs_depowner.objects.get(s_name=get_data_station['Филиал'][idx_data_station]),
                                     not_used=0)
            rwStation.save()
        # END_ЖД станция/участок----------------------------------------------------------------------------------------

        # BEGIN_ ЖД Пути------------------------------------------------------------------------------------------------
        data_path_way = f"static/bs/Пути.xlsx"  # файл с указанием названий филиалов
        get_data_way = pd.read_excel(data_path_way)
        for idx_data_way in get_data_way.index:
            rwway = Bs_RWway(s_mnemocode=get_data_way['Мнемокод'][idx_data_way],
                                     s_name=get_data_way['Название'][idx_data_way],
                                     s_create_user='auto_fill',
                                     idrwstation=Bs_RWStation.objects.get(s_name=get_data_way['Станция'][idx_data_way]),
                                     not_used=0)
            rwway.save()
        # END_ ЖД Пути--------------------------------------------------------------------------------------------------

        # # подразделения
        # objects = Bs_depowner.objects.filter(s_create_user='auto_fill')  # .only("s_name")  # only('s_name')
        # for x in objects:
        #     department = Bs_department(iddepowner=x, s_mnemocode='d', s_name='СПиМР', s_create_user='auto_fill', not_used=0)
        #     department.save()
        #     department = Bs_department(iddepowner=x, s_mnemocode='l', s_name='СЛХ', s_create_user='auto_fill', not_used=0)
        #     department.save()
        #     department = Bs_department(iddepowner=x, s_mnemocode='v', s_name='ВЧД', s_create_user='auto_fill', not_used=0)
        #     department.save()
        #     department = Bs_department(iddepowner=x, s_mnemocode='sh', s_name='ШЧ', s_create_user='auto_fill', not_used=0)
        #     department.save()
