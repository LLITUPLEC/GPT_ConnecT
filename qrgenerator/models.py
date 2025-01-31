from django.db import models
from django.forms import ModelChoiceField, Select
from smart_selects.db_fields import ChainedForeignKey

from BS.models import Bs_RWStation, Bs_depowner, Bs_RWsp, Bs_RWway


# Create your models here.

class Bar_code(models.Model):
    type_object = models.CharField('Тип объекта', max_length=8)
    src_bc = models.CharField('QR-код', max_length=18, null=True, blank=True)
    iddepowner = models.ForeignKey(Bs_depowner, on_delete=models.CASCADE, verbose_name='Филиал', default=None)
    station = ChainedForeignKey(Bs_RWStation, chained_field="iddepowner",
                                chained_model_field="iddepowner",
                                show_all=False,
                                auto_choose=True,
                                sort=True, null=True, blank=True)
    idrwsp = ChainedForeignKey(
        Bs_RWsp, chained_field="station",
        chained_model_field="idrwstation",
        show_all=False,
        auto_choose=True,
        sort=True, null=True, blank=True)
    idrwway = ChainedForeignKey(
        Bs_RWway,
        chained_field="station",
        chained_model_field="idrwstation",
        show_all=False,
        auto_choose=True,
        sort=True, null=True, blank=True)
    # station = models.ForeignKey(Bs_RWStation, on_delete=models.PROTECT, verbose_name='Станция', null=True, blank=True)
    s_create_user = models.CharField('Создатель', max_length=25)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True, editable=False)
    s_update_user = models.CharField('Изменивший', max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True, editable=False)

    def __str__(self):
        return str(self.type_object) + '(' + str(self.idrwsp) or str(self.idrwway) + ')' + ' ' + str(self.src_bc)

    class Meta:
        verbose_name = 'QR-код'
        verbose_name_plural = 'QR-коды'
