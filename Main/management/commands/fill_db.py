import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from BS.models import Bs_depowner, Bs_department, Bs_position, Bs_RWStation, Bs_Obj_insp, Bs_RW_element, \
    Bs_RW_defect_gr, Bs_RW_defect_tp, Bs_RWway, Bs_RWsp
from Main.models import Profile


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
        depart_path = f"static/bs/Подразделения.xlsx"  # файл с указанием названий подразделений
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
        position_path = f"static/bs/Должности.xlsx"  # файл с указанием названий должностей
        get_position = pd.read_excel(position_path)
        for idx_data in get_position.index:
            position = Bs_position(s_mnemocode=get_position['Мнемокод'][idx_data],
                                   s_name=get_position['Название'][idx_data],
                                   s_create_user='auto_fill',
                                   not_used=0)
            position.save()
        # END_Должность-------------------------------------------------------------------------------------------------

        # BEGIN_работники-----------------------------------------------------------------------------------------------
        worker_path = f"static/bs/Работники.xlsx"  # файл с указанием работников
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
        data_path_stations = f"static/bs/Станции.xlsx"  # файл с указанием названий станций
        get_data_station = pd.read_excel(data_path_stations)
        for idx_data_station in get_data_station.index:
            rwStation = Bs_RWStation(s_mnemocode=get_data_station['Мнемокод'][idx_data_station],
                                     s_name=get_data_station['Название'][idx_data_station],
                                     s_create_user='auto_fill',
                                     iddepowner=Bs_depowner.objects.get(
                                         s_name=get_data_station['Филиал'][idx_data_station]),
                                     not_used=0)
            rwStation.save()
        # END_ЖД станция/участок----------------------------------------------------------------------------------------

        # BEGIN_ ЖД Пути------------------------------------------------------------------------------------------------
        data_path_way = f"static/bs/Пути.xlsx"  # файл с указанием названий путей
        get_data_way = pd.read_excel(data_path_way)
        for idx_data_way in get_data_way.index:
            try:
                rwway = Bs_RWway(s_mnemocode=get_data_way['Мнемокод'][idx_data_way],
                                 s_name=get_data_way['Название'][idx_data_way],
                                 s_create_user='auto_fill',
                                 idrwstation=Bs_RWStation.objects.get(s_name=get_data_way['Станция'][idx_data_way]),
                                 not_used=0)
                rwway.save()
            except Exception as e:
                print(f"Exception occurred for value BEGIN_ ЖД Пути'" + "': " + repr(e))

        # END_ ЖД Пути--------------------------------------------------------------------------------------------------

        # BEGIN_ ЖД Стрелочные переводы---------------------------------------------------------------------------------
        data_path_sp = f"static/bs/Стрелочные переводы.xlsx"  # файл с указанием сп
        get_data_sp = pd.read_excel(data_path_sp)
        for idx_data_sp in get_data_sp.index:
            try:
                rwsp = Bs_RWsp(s_name=get_data_sp['№ стрелочного перевода'][idx_data_sp],
                               s_create_user='auto_fill',
                               idrwstation=Bs_RWStation.objects.get(s_name=get_data_sp['Станция'][idx_data_sp],
                                                                    iddepowner__s_name=get_data_sp['Филиал'][
                                                                        idx_data_sp]),
                               manag_method=get_data_sp['Способ управления'][idx_data_sp],
                               type_rail=get_data_sp['Тип рельсов'][idx_data_sp],
                               mark_crossp=get_data_sp['Марка крестовины'][idx_data_sp],
                               view_conversion=get_data_sp['Вид перевода'][idx_data_sp],
                               not_used=0)
                rwsp.save()
            except Exception as e:
                print(f"Exception occurred for value BEGIN_ ЖД Стрелочные переводы'" + "': " + repr(e))
        # END_ ЖД Стрелочные переводы-----------------------------------------------------------------------------------

        # BEGIN_ НЕИСПРАВНОСТИ      СП----------------------------------------------------------------------------------
        data_path = f"static/bs/классификатор СП.xlsx"  # файл с указанием названий объектов неисправностей
        get_data = pd.read_excel(data_path)
        # ==============================================================================================================
        # =====---------------Объекты осмотра-----------------------====================================================
        # ==============================================================================================================
        for obj in get_data['Объекты осмотра'].unique():
            # print(obj)
            try:
                obj_insp = Bs_Obj_insp(s_name=obj,
                                       s_mnemocode=f'obj_{obj[:2]}',
                                       s_create_user='auto_fill',
                                       iddepartment=Bs_department.objects.get(s_name='СП'),
                                       not_used=0)
                obj_insp.save()
            except Exception as e:
                print(f"Exception occurred for value BEGIN_ объекты осмотра'" + "': " + repr(e))
        # ==============================================================================================================
        # =====---------------Элементы осмотра----------------------====================================================
        # ==============================================================================================================
        res_el = (get_data.groupby(['Объекты осмотра', 'Осматриваемые элементы и характеристики'])
                  ['Неисправности или отклонения  от норм содержания (группы)']
                  .apply(lambda x: list(x.values))
                  .reset_index(name='info'))
        for idx_data_sp in res_el.index:
            try:
                el_insp = Bs_RW_element(s_name=res_el['Осматриваемые элементы и характеристики'][idx_data_sp],
                                        s_mnemocode=f'el_{idx_data_sp}',
                                        s_create_user='auto_fill',
                                        id_obj_insp=Bs_Obj_insp.objects.get(
                                            s_name=res_el['Объекты осмотра'][idx_data_sp]),
                                        not_used=0)
                el_insp.save()
            except Exception as e:
                print(f"Exception occurred for value BEGIN_ 'элементы' осмотра'" + "': " + repr(e))
        # ==============================================================================================================
        # =====-----------------Группы осмотра----------------------====================================================
        # ==============================================================================================================
        res_gr = (get_data.groupby(['Объекты осмотра',
                                    'Осматриваемые элементы и характеристики',
                                    'Неисправности или отклонения  от норм содержания (группы)'])
                  ['Неисправности или отклонения  от норм содержания (виды)']
                  .apply(lambda x: list(x.values))
                  .reset_index(name='info'))
        for idx_data_sp in res_gr.index:
            # print(res_gr['Объекты осмотра'][idx_data_sp], ' -> ',
            #       res_gr['Осматриваемые элементы и характеристики'][idx_data_sp].replace('  ', ' '), ' => ',
            #       res_gr['Неисправности или отклонения  от норм содержания (группы)'][idx_data_sp])

            try:
                gr_insp = Bs_RW_defect_gr(
                    s_name=res_gr['Неисправности или отклонения  от норм содержания (группы)'][idx_data_sp],
                    s_mnemocode=f'gr_{idx_data_sp}',
                    s_create_user='auto_fill',
                    id_rw_element=Bs_RW_element.objects.get(
                        s_name=res_gr['Осматриваемые элементы и характеристики'][idx_data_sp],
                        id_obj_insp=Bs_Obj_insp.objects.get(s_name=res_gr['Объекты осмотра'][idx_data_sp])),
                    not_used=0)
                gr_insp.save()
            except Exception as e:
                print(f"Exception occurred for value BEGIN_ 'элементы' осмотра'" + "': " + repr(e))
        # ==============================================================================================================
        # =====-----------------Виды осмотра (сама неисправность)---====================================================
        # ==============================================================================================================
        get_data = get_data.fillna('-')

        count = 1
        for idx_data_sp in get_data.index:
            print(count, ' : ',
                  get_data['Неисправности или отклонения  от норм содержания (виды)'][idx_data_sp], ' => ',
                  get_data['Интервал отклонения'][idx_data_sp], get_data['Интервал отклонения2'][idx_data_sp],
                  get_data['Крайний срок (в днях)'][idx_data_sp], get_data['Единица измерения'][idx_data_sp],
                  get_data['Ограничение скорости'][idx_data_sp]
                  )

            count += 1
            try:
                type_insp = Bs_RW_defect_tp(
                    s_name=get_data['Неисправности или отклонения  от норм содержания (виды)'][idx_data_sp],  # ++
                    s_mnemocode=f'type_{idx_data_sp}',
                    s_create_user='auto_fill',
                    id_RW_defect_gr=Bs_RW_defect_gr.objects.get(
                        s_name=get_data['Неисправности или отклонения  от норм содержания (группы)'][idx_data_sp],
                        id_rw_element=Bs_RW_element.objects.get(s_name=get_data['Осматриваемые элементы и характеристики'][idx_data_sp],
                                                                id_obj_insp=Bs_Obj_insp.objects.get(s_name=get_data['Объекты осмотра'][idx_data_sp]))
                    ),
                    s_deviation_interval=get_data['Интервал отклонения'][idx_data_sp],
                    s_deviation_interval_dop=get_data['Интервал отклонения2'][idx_data_sp],
                    d_deadline=get_data['Крайний срок (в днях)'][idx_data_sp],
                    s_measurement=get_data['Единица измерения'][idx_data_sp],
                    n_speed_limit=get_data['Ограничение скорости'][idx_data_sp],
                    not_used=0)
                type_insp.save()
            except Exception as e:
                print(f"Exception occurred for value BEGIN_ 'элементы' осмотра'" + "': " + repr(e))

        # END_ НЕИСПРАВНОСТИ      СП------------------------------------------------------------------------------------

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
