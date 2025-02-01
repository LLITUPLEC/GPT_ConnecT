# from main.models import Profile
from smart_selects.db_fields import ChainedForeignKey

from BS.models import Bs_depowner, Bs_RWStation, Bs_RWsp, Bs_RWway
from qrgenerator.models import Bar_code
from django.forms import (ModelForm, Select, ModelChoiceField, TextInput,
                          ChoiceField, modelformset_factory, forms, CheckboxInput, Textarea, ImageField, CharField)

typeObj_CHOICES = (
    ('', '---------'),
    ('stp', 'Стрелочный перевод'),
    ('way', 'Путь'),
)
class QR_create(ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['idrwsp'].queryset = Bs_RWsp.objects.filter(pk=1)
    #

    class Meta:
        model = Bar_code
        fields = ["type_object",
                  "src_bc",
                  "iddepowner",
                  "station",
                  "idrwsp",
                  "idrwway",
                  ]

    type_object = ChoiceField(choices=typeObj_CHOICES,
                          widget=Select(attrs={'class': 'form-control', 'placeholder': 'Выберите объект', 'required': 'required'}))

    iddepowner = ModelChoiceField(queryset=Bs_depowner.objects.all(),
                                  widget=Select(attrs={'class': 'form-select', 'placeholder': 'выберите филиал'}))
    station = ChainedForeignKey(Bs_RWStation, chained_field="iddepowner",
                                chained_model_field="iddepowner",
                                show_all=False,
                                auto_choose=True,
                                sort=True, null=True, blank=True)
    idrwsp = ChainedForeignKey(
        Bs_RWsp,
        chained_field="station",
        chained_model_field="idrwstation",
        show_all=False,
        auto_choose=True,
        sort=True, null=True, blank=True
    )
    idrwway = ChainedForeignKey(
        Bs_RWway,
        chained_field="station",
        chained_model_field="idrwstation",
        show_all=False,
        auto_choose=True,
        sort=True, null=True, blank=True
    )
    # station = ModelChoiceField(queryset=Bs_RWStation.objects.all(),
    #                             widget=Select(attrs={'class': 'form-select', 'placeholder': 'выберите филиал'}))
    # src_bc = ModelChoiceField(queryset=Profile.objects.filter(chairman=True),
    #                              widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите председателя'}))




