# from main.models import Profile
from .models import Kmo, Kmo_members, Kmodet, picket_CHOICES, zveno_CHOICES, thread_CHOICES
from Main.models import Profile
from BS.models import *
from KMO.models import Kmo_responsible
from django.forms import (ModelForm, Select, ModelChoiceField, TextInput,
                          ChoiceField, modelformset_factory, forms, CheckboxInput, Textarea, ImageField, CharField)
from smart_selects.db_fields import ChainedForeignKey


class KMO_check_create(ModelForm):
    class Meta:
        model = Kmo
        fields = ["iddepowner",
                  "user_creator",
                  "n_regnumber",
                  "date_detection",
                  # "image_defect",
                  # "s_update_user",
                  # "idprofile",
                  ]
        widgets = {
            "n_regnumber": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите регистрационный номер',
                'readonly': 'readonly'
            }),
            "user_creator": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите создателя',
                'readonly': 'readonly'
            }),
            'date_detection': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Укажите дату', 'type': 'date'}),
        }

    iddepowner = ModelChoiceField(queryset=Bs_depowner.objects.all(),
                                  widget=Select(attrs={'class': 'form-select', 'placeholder': 'выберите филиал'}))

    def check_kmo_date_and_dep(self):
        depowner = self.cleaned_data.get('iddepowner')  # получаем филиал из формы
        date_object = str(self.cleaned_data.get('date_detection'))[:7]  # получаем дату КМО из формы
        # а тут запрос к БД, сколько КМО по таким полям(филиал и дата). Должно быть 0, чтобы создать новый КМО
        has_act = Kmo.objects.filter(iddepowner=Bs_depowner.objects.get(s_name=str(depowner))
                                     , date_detection__icontains=date_object
                                     ).count()

        print('has_act => ', has_act)
        if has_act > 0:
            return 'error_date_dep'
        else:
            return depowner


class KMOForm(ModelForm):
    class Meta:
        model = Kmo
        fields = ["iddepowner",
                  "user_creator",
                  "n_regnumber",
                  "date_detection",
                  # "image_defect",
                  "s_update_user",
                  # "idprofile",
                  ]
        widgets = {
            "n_regnumber": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите регистрационный номер',
                'readonly': 'readonly'
            }),
            "user_creator": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите создателя',
                'readonly': 'readonly'
            }),
            'date_detection': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Укажите дату', 'type': 'date'}),
        }

    iddepowner = ModelChoiceField(queryset=Bs_depowner.objects.all(),
                                  widget=Select(attrs={'class': 'form-select', 'placeholder': 'выберите филиал'}))
    idprofile = ModelChoiceField(queryset=Profile.objects.filter(chairman=True),
                                 widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите председателя'}))

    def check_kmo_date_and_dep(self):
        depowner = self.cleaned_data.get('iddepowner')  # получаем филиал из формы
        date_object = str(self.cleaned_data.get('date_detection'))[:7]  # получаем дату КМО из формы
        # а тут запрос к БД, сколько КМО по таким полям(филиал и дата). Должно быть 0, чтобы создать новый КМО
        has_act = Kmo.objects.filter(iddepowner=Bs_depowner.objects.get(s_name=str(depowner))
                                     , date_detection__icontains=date_object
                                     ).exclude(id=48).count()

        print('has_act => ', has_act)
        if has_act > 0:
            raise forms.ValidationError("КМО в данном периоде и филиале уже существует")
        else:
            return depowner


class KMOForm_edit(ModelForm):
    class Meta:
        model = Kmo
        fields = [  #"iddepowner",
            # "user_creator",
            "s_update_user",
            #"n_regnumber",
            #"date_detection",
            "idprofile",
        ]

    # n_regnumber = CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'рег №'}))
    # date_detection = CharField(required=False, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'дата проведения', 'type': 'date'}))
    # iddepowner = ModelChoiceField(queryset=Bs_depowner.objects.all(),
    #                               widget=Select(attrs={'class': 'form-select', 'placeholder': 'выберите филиал'}))
    idprofile = ModelChoiceField(queryset=Profile.objects.filter(chairman=True), required=False,
                                 widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите председателя'}))

    # def check_kmo_date_and_dep(self, kmo_id):
    #
    #     depowner = self.cleaned_data.get('iddepowner')  # получаем филиал из формы
    #     date_object = str(self.cleaned_data.get('date_detection'))[:7]  # получаем дату КМО из формы
    #     # а тут запрос к БД, сколько КМО по таким полям(филиал и дата). Должно быть 0, чтобы создать новый КМО
    #     has_act = Kmo.objects.filter(iddepowner=Bs_depowner.objects.get(s_name=str(depowner))
    #                                  , date_detection__icontains=date_object
    #                                  ).exclude(id=kmo_id).count()
    #
    #     print('has_act => ', has_act)
    #     if has_act > 0:
    #         return 'error_date_dep'
    #     else:
    #         return depowner


Kmo_membersFormSet = modelformset_factory(
    Kmo_members, fields=("idkmo", "idprofile"), extra=1
)


class KMOdetForm_create1(ModelForm):
    class Meta:
        model = Kmodet
        fields = ["idkmo",
                  "user_creator",
                  "iddepowner",
                  "date_detection",
                  "iddepartment",
                  "s_update_user",
                  "idrwstation",
                  "idrwstage",
                  "idrwway",
                  "idrwkilometr",
                  "idrwsp",
                  "RW_picket",
                  "RW_unit",
                  "RW_thread",
                  "idBs_Obj_insp",
                  "idBs_RW_element",
                  "idBs_RW_defect_gr",
                  "idBs_RW_defect_tp",
                  "RW_size_def",
                  "date_elimination",
                  "date_elimination_edit",
                  "image_defect",
                  "eliminated",
                  "comment",
                  "idresponsible",
                  ]
        widgets = {
            # "n_regnumber": TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Введите регистрационный номер',
            #     'readonly': 'readonly'
            # }),
            # "user_creator": TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Укажите создателя',
            #     'readonly': 'readonly'
            # }),
            'date_detection': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Укажите дату', 'type': 'date'}),
            'date_elimination': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Срок устранения', 'type': 'date'}),
            'date_elimination_edit': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Срок устранения изменить', 'type': 'date'}),
            "RW_size_def": TextInput(attrs={
                'class': 'form-control', 'type': 'select'
            }),
            "eliminated": CheckboxInput(),
            "comment": Textarea(attrs={
                'class': "form-control", 'id': "exampleFormControlTextarea1", 'rows': "3"}),

        }

    RW_picket = ChoiceField(choices=picket_CHOICES,
                            widget=Select(attrs={'class': 'form-control', 'placeholder': 'укажите пикет'}))
    RW_unit = ChoiceField(choices=zveno_CHOICES,
                          widget=Select(attrs={'class': 'form-control', 'placeholder': 'укажите звено'}))
    RW_thread = ChoiceField(choices=thread_CHOICES,
                            widget=Select(attrs={'class': 'form-control', 'placeholder': 'укажите ветку'}))
    idrwstation = ModelChoiceField(queryset=Bs_RWStation.objects.all(),
                                   widget=Select(attrs={'class': 'form-select', 'placeholder': 'выберите станцию'}))
    idrwstage = ModelChoiceField(queryset=Bs_RWstage.objects.all(),
                                 widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите перегон'}),
                                 required=False)
    idrwway = ModelChoiceField(queryset=Bs_RWway.objects.select_related('idrwstation'),
                               widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите путь'}),
                               required=False)
    idrwsp = ModelChoiceField(queryset=Bs_RWsp.objects.all(),
                              widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите стр.перевод'}),
                              required=False)
    idrwkilometr = ModelChoiceField(queryset=Bs_RWkilometr.objects.all(),
                                    widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите км'}),
                                    required=False)

    idBs_Obj_insp = ModelChoiceField(queryset=Bs_Obj_insp.objects.all(),
                                     widget=Select(attrs={'class': 'form-select'}))
    idBs_RW_element = ModelChoiceField(queryset=Bs_RW_element.objects.all(),
                                       widget=Select(attrs={'class': 'form-select'}))
    idBs_RW_defect_gr = ModelChoiceField(queryset=Bs_RW_defect_gr.objects.all(),
                                         widget=Select(attrs={'class': 'form-select'}))
    idBs_RW_defect_tp = ModelChoiceField(queryset=Bs_RW_defect_tp.objects.all(),
                                         widget=Select(attrs={'class': 'form-select'}))
    # iddepartment = ModelChoiceField(queryset=Bs_department.objects.all(),
    #                                widget=Select(attrs={'class': 'form-select', 'placeholder': 'выберите подразделение'}))
    idresponsible = ModelChoiceField(queryset=Kmo_responsible.objects.all(),
                                     widget=Select(
                                         attrs={'class': 'form-select', 'placeholder': 'выберите ответственного'}))


class KMOdetForm_create(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        iddepart = Bs_depowner.objects.filter(s_name=self.instance.iddepowner).first()
        self.fields['idrwstation'].queryset = Bs_RWStation.objects.filter(iddepowner=iddepart)

    class Meta:
        model = Kmodet
        fields = ["idkmo",
                  # "user_creator",
                  "iddepowner",
                  "date_detection",
                  "iddepartment",
                  "s_update_user",
                  "idrwstation",
                  "idrwstage",
                  "idrwway",
                  "idrwkilometr",
                  "idrwsp",
                  "RW_picket",
                  "RW_unit",
                  "RW_thread",
                  "idBs_Obj_insp",
                  "idBs_RW_element",
                  "idBs_RW_defect_gr",
                  "idBs_RW_defect_tp",
                  "RW_size_def",
                  "date_elimination",
                  "date_elimination_edit",
                  "image_defect",
                  # "eliminated",
                  "comment",
                  "idresponsible",
                  ]
        widgets = {
            # "n_regnumber": TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Введите регистрационный номер',
            #     'readonly': 'readonly'
            # }),
            # "user_creator": TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Укажите создателя',
            #     'readonly': 'readonly'
            # }),
            'date_detection': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Укажите дату', 'type': 'date'}),
            'date_elimination': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Срок устранения', 'type': 'date'}),
            'date_elimination_edit': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Срок устранения изменить', 'type': 'date'}),
            "iddepartment": TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            "RW_size_def": TextInput(attrs={
                'class': 'form-control'
            }),
            "comment": Textarea(attrs={
                'class': "form-control", 'id': "exampleFormControlTextarea1", 'rows': "3"}),
            # "eliminated": CheckboxInput(),

        }

    RW_picket = ChoiceField(choices=picket_CHOICES,
                            widget=Select(attrs={'class': 'form-control', 'placeholder': 'укажите пикет'}))
    RW_unit = ChoiceField(choices=zveno_CHOICES,
                          widget=Select(attrs={'class': 'form-control', 'placeholder': 'укажите звено'}))
    RW_thread = ChoiceField(choices=thread_CHOICES,
                            widget=Select(attrs={'class': 'form-control', 'placeholder': 'укажите ветку'}))
    # RW_thread = ChoiceField(choices=thread_CHOICES, widget=RadioSelect)

    idrwstation = ModelChoiceField(queryset=Bs_RWStation.objects.all(),
                                   widget=Select(attrs={'class': 'form-select', 'placeholder': 'выберите станцию'}))
    idrwstage = ModelChoiceField(queryset=Bs_RWstage.objects.all(),
                                 widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите перегон'}),
                                 required=False)
    # idrwway = ModelChoiceField(queryset=Bs_RWway.objects.none(),
    #                              widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите путь'}))
    idrwway = ChainedForeignKey(
        Bs_RWway,
        chained_field="idrwstation",
        chained_model_field="idrwstation",
        show_all=False,
        auto_choose=True,
        sort=True,
    )
    # idrwsp = ModelChoiceField(queryset=Bs_RWsp.objects.all(),
    #                              widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите стр.перевод'}))
    idrwsp = ChainedForeignKey(
        Bs_RWsp, chained_field="idrwstation",
        chained_model_field="idrwsp",
        show_all=False,
        auto_choose=True,
        sort=True)
    idrwkilometr = ModelChoiceField(queryset=Bs_RWkilometr.objects.all(),
                                    widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите км'}))

    idBs_Obj_insp = ModelChoiceField(queryset=Bs_Obj_insp.objects.all(),
                                     widget=Select(attrs={'class': 'form-select'}))
    idBs_RW_element = ModelChoiceField(queryset=Bs_RW_element.objects.all(),
                                       widget=Select(attrs={'class': 'form-select'}))
    idBs_RW_defect_gr = ModelChoiceField(queryset=Bs_RW_defect_gr.objects.all(),
                                         widget=Select(attrs={'class': 'form-select'}))
    idBs_RW_defect_tp = ModelChoiceField(queryset=Bs_RW_defect_tp.objects.all(),
                                         widget=Select(attrs={'class': 'form-select'}))
    idresponsible = ModelChoiceField(queryset=Kmo_responsible.objects.all(),
                                     widget=Select(
                                         attrs={'class': 'form-select', 'placeholder': 'выберите ответственного'}))


class KMOdetForm_edit(ModelForm):
    class Meta:
        model = Kmodet
        fields = ["idkmo",
                  # "user_creator",
                  "iddepowner",
                  "date_detection",
                  "iddepartment",
                  "s_update_user",
                  "idrwstation",
                  "idrwstage",
                  "idrwway",
                  "idrwkilometr",
                  "idrwsp",
                  "RW_picket",
                  "RW_unit",
                  "RW_thread",
                  "idBs_Obj_insp",
                  "idBs_RW_element",
                  "idBs_RW_defect_gr",
                  "idBs_RW_defect_tp",
                  "RW_size_def",
                  "date_elimination",
                  "date_elimination_edit",
                  "image_defect",
                  "eliminated",
                  "comment",
                  "idresponsible",
                  ]
        widgets = {
            # "n_regnumber": TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Введите регистрационный номер',
            #     'readonly': 'readonly'
            # }),
            # "user_creator": TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Укажите создателя',
            #     'readonly': 'readonly'
            # }),
            'date_detection': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Укажите дату', 'type': 'date'}),
            'date_elimination': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Срок устранения', 'type': 'date'}),
            'date_elimination_edit': TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Срок устранения изменить', 'type': 'date'}),
            "iddepartment": TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            "RW_size_def": TextInput(attrs={
                'class': 'form-control'
            }),
            "comment": Textarea(attrs={
                'class': "form-control", 'id': "exampleFormControlTextarea1", 'rows': "3"}),
            "eliminated": CheckboxInput(),

        }

    RW_picket = ChoiceField(choices=picket_CHOICES,
                            widget=Select(attrs={'class': 'form-control', 'placeholder': 'укажите пикет'}))
    RW_unit = ChoiceField(choices=zveno_CHOICES,
                          widget=Select(attrs={'class': 'form-control', 'placeholder': 'укажите звено'}))
    RW_thread = ChoiceField(choices=thread_CHOICES,
                            widget=Select(attrs={'class': 'form-control', 'placeholder': 'укажите ветку'}))
    # RW_thread = ChoiceField(choices=thread_CHOICES, widget=RadioSelect)

    idrwstation = ModelChoiceField(queryset=Bs_RWStation.objects.all(),
                                   widget=Select(attrs={'class': 'form-select', 'placeholder': 'выберите станцию'}))
    idrwstage = ModelChoiceField(queryset=Bs_RWstage.objects.all(),
                                 widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите перегон'}),
                                 required=False)
    # idrwway = ModelChoiceField(queryset=Bs_RWway.objects.none(),
    #                              widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите путь'}))
    idrwway = ChainedForeignKey(
        Bs_RWway,
        chained_field="idrwstation",
        chained_model_field="idrwstation",
        show_all=False,
        auto_choose=True,
        sort=True,
    )
    idrwsp = ModelChoiceField(queryset=Bs_RWsp.objects.all(),
                              widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите стр.перевод'}))
    idrwkilometr = ModelChoiceField(queryset=Bs_RWkilometr.objects.all(),
                                    widget=Select(attrs={'class': 'form-select', 'placeholder': 'укажите км'}))

    idBs_Obj_insp = ModelChoiceField(queryset=Bs_Obj_insp.objects.all(),
                                     widget=Select(attrs={'class': 'form-select'}))
    idBs_RW_element = ModelChoiceField(queryset=Bs_RW_element.objects.all(),
                                       widget=Select(attrs={'class': 'form-select'}))
    idBs_RW_defect_gr = ModelChoiceField(queryset=Bs_RW_defect_gr.objects.all(),
                                         widget=Select(attrs={'class': 'form-select'}))
    idBs_RW_defect_tp = ModelChoiceField(queryset=Bs_RW_defect_tp.objects.all(),
                                         widget=Select(attrs={'class': 'form-select'}))
    idresponsible = ModelChoiceField(queryset=Kmo_responsible.objects.all(),
                                     widget=Select(
                                         attrs={'class': 'form-select', 'placeholder': 'выберите ответственного'}))
