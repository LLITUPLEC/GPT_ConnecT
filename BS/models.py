from django.db import models
from datetime import datetime


class Bs_depowner(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=10)
    s_name = models.CharField('Филиал', max_length=30)
    s_create_user = models.CharField('Создатель', max_length=25)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)

    def __str__(self):
        return self.s_name

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'


class Bs_department(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=10)
    s_name = models.CharField('Подразделение', max_length=50)
    # iddepowner = models.ForeignKey(Bs_depowner, on_delete=models.CASCADE, verbose_name='Филиал')
    s_create_user = models.CharField('Создатель', max_length=25)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)
    part_kmo = models.BooleanField('Участвует в КМО', default=False)

    def __str__(self):
        return self.s_name

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'


class Bs_position(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=10)
    s_name = models.CharField('Должность', max_length=90)
    # iddepartment = models.ForeignKey(Bs_department, on_delete=models.CASCADE, verbose_name='Подразделение')
    s_create_user = models.CharField('Создатель', max_length=25)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)

    def __str__(self):
        return self.s_name

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Bs_RWStation(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=10)
    s_name = models.CharField('Станция/Участок', max_length=70)
    iddepowner = models.ForeignKey(Bs_depowner, on_delete=models.CASCADE, verbose_name='Филиал', default=None)
    s_create_user = models.CharField('Создатель', max_length=25)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)

    def __str__(self):
        return self.s_name

    class Meta:
        verbose_name = 'ЖД станция/участок'
        verbose_name_plural = 'ЖД станции/участки'


class Bs_RWway(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=10, blank=True, null=True)
    s_name = models.CharField('Путь', max_length=10)
    idrwstation = models.ForeignKey(Bs_RWStation, on_delete=models.SET_NULL, verbose_name='Станция/участок', null=True)
    s_create_user = models.CharField('Создатель', max_length=25)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)

    def __str__(self):
        return str(self.s_name) + '(' + str(self.idrwstation) + ')'

    class Meta:
        verbose_name = 'ЖД путь'
        verbose_name_plural = 'ЖД пути'


class Bs_RWkilometr(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=10, blank=True, null=True)
    s_name = models.CharField('км', max_length=6)
    idrwstation = models.ForeignKey(Bs_RWStation, on_delete=models.SET_NULL, verbose_name='Станция/участок', null=True)
    s_create_user = models.CharField('Создатель', max_length=25)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)

    def __str__(self):
        return str(self.s_name) + 'км(' + str(self.idrwstation) + ')'

    class Meta:
        verbose_name = 'км станции'
        verbose_name_plural = 'км-ы станции'


class Bs_RWstage(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=10, blank=True, null=True)
    left_border = models.ForeignKey(Bs_RWStation, on_delete=models.SET_NULL, verbose_name='Чётная граница',
                                    related_name='left_border', null=True)
    right_border = models.ForeignKey(Bs_RWStation, on_delete=models.SET_NULL, verbose_name='Нечётная граница',
                                     related_name='right_border', null=True)
    s_create_user = models.CharField('Создатель', max_length=25)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)

    def __str__(self):
        return str(self.left_border) + ' - ' + str(self.right_border)

    class Meta:
        verbose_name = 'ЖД перегон'
        verbose_name_plural = 'ЖД перегоны'

class Bs_RWsp(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=10, blank=True, null=True)
    s_name = models.CharField('Стрелочный перевод', max_length=8)
    idrwstation = models.ForeignKey(Bs_RWStation, on_delete=models.SET_NULL, verbose_name='Станция', null=True)
    manag_method = models.CharField('Способ управления', max_length=15, default="Неопределенно")
    type_rail = models.CharField('Тип рельсов', max_length=8, default="Неопределенно")
    mark_crossp = models.CharField('Марка крестовины', max_length=8, default="Неопределенно")
    view_conversion = models.CharField('Вид перевода', max_length=20, default="Неопределенно")
    s_create_user = models.CharField('Создатель', max_length=25)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)

    def __str__(self):
        return str(self.s_name) + ' ' + str(self.mark_crossp)

    class Meta:
        verbose_name = 'Стрелочный перевод'
        verbose_name_plural = 'Стрелочные переводы'

# 1 столбец
class Bs_Obj_insp(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=12)
    s_name = models.CharField('Объекты  осмотра', max_length=40)
    iddepartment = models.ForeignKey(Bs_department, on_delete=models.SET_NULL, verbose_name='Служба', null=True)
    s_create_user = models.CharField('Создатель', max_length=35)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=35, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)

    def __str__(self):
        return self.s_name

    class Meta:
        verbose_name = 'Объект  осмотра'
        verbose_name_plural = 'Объекты  осмотра'


# 2 столбец
class Bs_RW_element(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=12)
    s_name = models.CharField('Элемент осмотра', max_length=40)
    id_obj_insp = models.ForeignKey(Bs_Obj_insp, on_delete=models.CASCADE, verbose_name='Объект осмотра')
    s_create_user = models.CharField('Создатель', max_length=35)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=35, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)

    def __str__(self):
        return self.s_name

    class Meta:
        verbose_name = 'Элемент осмотра'
        verbose_name_plural = 'Элементы осмотра'


# 3 столбец
class Bs_RW_defect_gr(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=12)
    s_name = models.CharField('Группа Неисправности', max_length=250)
    id_rw_element = models.ForeignKey(Bs_RW_element, on_delete=models.CASCADE, verbose_name='Элемент осмотра')
    s_create_user = models.CharField('Создатель', max_length=35)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=35, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False)

    def __str__(self):
        return self.s_name

    class Meta:
        verbose_name = 'Группа Неисправности или отклонения'
        verbose_name_plural = 'Группа Неисправностей или отклонений'


class Bs_RW_defect_tp(models.Model):
    s_mnemocode = models.CharField('мнемокод', max_length=10)
    id_RW_defect_gr = models.ForeignKey(Bs_RW_defect_gr, on_delete=models.CASCADE, verbose_name='Группа Неисправности')
    s_name = models.CharField('Вид неисправности', max_length=350)
    s_deviation_interval = models.CharField('Интервал отклонения', max_length=15, null=True, blank=True)
    s_deviation_interval_dop = models.CharField('Интервал отклонения_2', max_length=15, null=True, blank=True)
    d_deadline = models.CharField('Крайний срок (в днях)', max_length=10, null=True)
    s_measurement = models.CharField('Единица измерения',
                                     max_length=10, null=True, blank=True)  # сделать потом отдельный справочник по единицам измерения
    n_speed_limit = models.CharField('Ограничение скорости', max_length=5, null=True, blank=True)
    s_create_user = models.CharField('Создатель', max_length=25, null=True, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    not_used = models.BooleanField('Недействующий', default=False, null=True, blank=True)

    def __str__(self):
        return (str(self.s_name) +
                ' [ ' + str(self.s_deviation_interval) +
                ' | ' + str(self.d_deadline) +
                ' | ' + str(self.s_measurement) +
                ' | ' + str(self.n_speed_limit) + ']')

    class Meta:
        verbose_name = 'Вид Неисправности или отклонения'
        verbose_name_plural = 'Вид Неисправностей или отклонений'
