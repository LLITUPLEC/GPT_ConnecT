from os.path import splitext

from django.db import models
from BS.models import (Bs_Obj_insp, Bs_depowner, Bs_department, Bs_RWStation,
                       Bs_RW_element, Bs_RW_defect_gr, Bs_RW_defect_tp,
                       Bs_RWstage, Bs_RWway, Bs_RWkilometr, Bs_RWsp)
from Main.models import Profile


picket_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )

zveno_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
thread_CHOICES = (
        ('r', 'правая'),
        ('l', 'левая'),
    )
class Kmo_responsible(models.Model):
    iddepowner = models.ForeignKey(Bs_depowner, on_delete=models.CASCADE, verbose_name='На филиале')
    iddepartment = models.ForeignKey(Bs_department, on_delete=models.CASCADE, verbose_name='По службе')
    idprofile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Ответственный')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    user_creator = models.CharField('Создатель', max_length=50, null=True, blank=True)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)

    def __str__(self):
        return str(self.idprofile) + '(' + str(self.iddepartment) + ')'

    class Meta:
        verbose_name = 'Ответственный за устранение'
        verbose_name_plural = 'Список ответственных за устранение'

class Kmo(models.Model):
    iddepowner = models.ForeignKey(Bs_depowner, on_delete=models.CASCADE, verbose_name='Филиал')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    user_creator = models.CharField('Создатель', max_length=50, null=True, blank=True)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    n_regnumber = models.CharField('Рег. №', max_length=12)
    date_detection = models.DateField('Дата обнаружения')
    idprofile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Председатель', null=True)

    def __str__(self):
        return 'КМО Рег. №' + str(self.n_regnumber) + 'от ' + str(self.date_detection) + '(' + str(
            self.iddepowner) + ') [' + str(self.created_at) + ']'

    class Meta:
        verbose_name = 'КМО'
        verbose_name_plural = 'Список КМО'


class Kmodet(models.Model):
    idkmo = models.ForeignKey(Kmo, on_delete=models.CASCADE, verbose_name='КМО')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    user_creator = models.CharField('Создатель', max_length=50, null=True, blank=True)
    s_update_user = models.CharField('Изменивший', max_length=50, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    date_detection = models.DateField('Дата обнаружения')

    iddepartment = models.ForeignKey(Bs_department, on_delete=models.CASCADE, verbose_name='Подразделение')
    idrwstation = models.ForeignKey(Bs_RWStation, on_delete=models.CASCADE, verbose_name='Станция/Участок', null=True, blank=True)
    idrwstage = models.ForeignKey(Bs_RWstage, on_delete=models.CASCADE, verbose_name='Перегон', null=True, blank=True, default=None)
    idrwway = models.ForeignKey(Bs_RWway, on_delete=models.CASCADE, verbose_name='Путь', null=True, blank=True, default=None)
    idrwkilometr = models.ForeignKey(Bs_RWkilometr, on_delete=models.CASCADE, verbose_name='км', null=True, blank=True, default=None)
    idrwsp = models.ForeignKey(Bs_RWsp, on_delete=models.CASCADE, verbose_name='Стрелочный перевод', null=True, blank=True, default=None)

    RW_picket = models.CharField(max_length=2, choices=picket_CHOICES, verbose_name='пикет')
    RW_unit = models.CharField('Звено', choices=zveno_CHOICES, max_length=2)
    RW_thread = models.CharField('Нитка', choices=thread_CHOICES, max_length=2)

    idBs_Obj_insp = models.ForeignKey(Bs_Obj_insp, on_delete=models.CASCADE, verbose_name='Объект осмотра')
    idBs_RW_element = models.ForeignKey(Bs_RW_element, on_delete=models.CASCADE, verbose_name='Элемент осмотра')
    idBs_RW_defect_gr = models.ForeignKey(Bs_RW_defect_gr, on_delete=models.CASCADE,
                                          verbose_name='Группа Неисправности')
    idBs_RW_defect_tp = models.ForeignKey(Bs_RW_defect_tp, on_delete=models.CASCADE, verbose_name='Вид неисправности')
    RW_size_def = models.CharField('Величина неисправности', max_length=100, default=None)

    date_elimination = models.DateField('Срок устранения')
    date_elimination_edit = models.DateField('Срок устранения изменить', null=True, blank=True)
    # image_defect = models.ImageField('Фотография неисправности', blank=True, upload_to='kmo_imgs')
    image_defect = models.ImageField('Фотография неисправности', blank=True, upload_to=lambda obj, name: 'kmo_imgs/' + str(obj.idkmo.date_detection)[:7] + '/' + str(name))


    eliminated = models.BooleanField('Устранено', default=False, null=True, blank=True)
    comment = models.CharField('Комментарий к замечанию', max_length=4000, null=True, blank=True)

    idresponsible = models.ForeignKey(Kmo_responsible, on_delete=models.CASCADE, verbose_name='Ответственный за  устранение', default=None)

    def __str__(self):
        return 'Неисправность: "' + str(self.idBs_RW_defect_tp) + '" | Служба: "' + str(self.iddepartment) + '" | Акт: [' + str(
            self.idkmo) + '] | Срок устранения - [' + str(self.date_elimination) + ']'

    class Meta:
        verbose_name = 'позиция КМО'
        verbose_name_plural = 'Список позиций КМО'

class Kmo_members(models.Model):
    idkmo = models.ForeignKey(Kmo, on_delete=models.CASCADE, verbose_name='КМО', blank=True, null=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    user_creator = models.CharField('Создатель', max_length=50, null=True, blank=True)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)
    idprofile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Член комиссии', default=None, null=True, blank=True)

    def __str__(self):
        return str(self.idprofile)

    class Meta:
        verbose_name = 'Члены комиссии КМО'
        verbose_name_plural = 'Список членов комиссии КМО'



