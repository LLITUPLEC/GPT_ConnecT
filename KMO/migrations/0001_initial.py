# Generated by Django 5.1.4 on 2025-01-28 20:18

import KMO.models
import django.db.models.deletion
import smart_selects.db_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('BS', '0001_initial'),
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kmo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user_creator', models.CharField(blank=True, max_length=50, null=True, verbose_name='Создатель')),
                ('s_update_user', models.CharField(blank=True, max_length=25, null=True, verbose_name='Изменивший')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('n_regnumber', models.CharField(max_length=12, verbose_name='Рег. №')),
                ('date_detection', models.DateField(verbose_name='Дата обнаружения')),
                ('approved', models.BooleanField(blank=True, default=False, null=True, verbose_name='Утверждён')),
                ('iddepowner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BS.bs_depowner', verbose_name='Филиал')),
                ('idprofile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.profile', verbose_name='Председатель')),
            ],
            options={
                'verbose_name': 'КМО',
                'verbose_name_plural': 'Список КМО',
            },
        ),
        migrations.CreateModel(
            name='Kmo_members',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user_creator', models.CharField(blank=True, max_length=50, null=True, verbose_name='Создатель')),
                ('s_update_user', models.CharField(blank=True, max_length=25, null=True, verbose_name='Изменивший')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('idkmo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='KMO.kmo', verbose_name='КМО')),
                ('idprofile', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Main.profile', verbose_name='Член комиссии')),
            ],
            options={
                'verbose_name': 'Члены комиссии КМО',
                'verbose_name_plural': 'Список членов комиссии КМО',
            },
        ),
        migrations.CreateModel(
            name='Kmo_responsible',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user_creator', models.CharField(blank=True, max_length=50, null=True, verbose_name='Создатель')),
                ('s_update_user', models.CharField(blank=True, max_length=25, null=True, verbose_name='Изменивший')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('iddepartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BS.bs_department', verbose_name='По службе')),
                ('iddepowner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BS.bs_depowner', verbose_name='На филиале')),
                ('idprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.profile', verbose_name='Ответственный')),
            ],
            options={
                'verbose_name': 'Ответственный за устранение',
                'verbose_name_plural': 'Список ответственных за устранение',
            },
        ),
        migrations.CreateModel(
            name='Kmodet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user_creator', models.CharField(blank=True, max_length=50, null=True, verbose_name='Создатель')),
                ('s_update_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='Изменивший')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('date_detection', models.DateField(verbose_name='Дата обнаружения')),
                ('RW_picket', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=2, verbose_name='пикет')),
                ('RW_unit', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=2, verbose_name='Звено')),
                ('RW_thread', models.CharField(choices=[('правая', 'правая'), ('правая', 'левая')], max_length=6, verbose_name='Нитка')),
                ('RW_size_def', models.CharField(default=None, max_length=100, verbose_name='Величина неисправности')),
                ('date_elimination', models.DateField(verbose_name='Срок устранения')),
                ('date_elimination_edit', models.DateField(blank=True, null=True, verbose_name='Срок устранения изменить')),
                ('image_defect', models.ImageField(blank=True, upload_to=KMO.models.custom_path, verbose_name='Фотография неисправности')),
                ('eliminated', models.BooleanField(blank=True, default=False, null=True, verbose_name='Устранено')),
                ('comment', models.CharField(blank=True, max_length=4000, null=True, verbose_name='Комментарий к замечанию')),
                ('idBs_Obj_insp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BS.bs_obj_insp', verbose_name='Объект осмотра')),
                ('idBs_RW_defect_gr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BS.bs_rw_defect_gr', verbose_name='Группа Неисправности')),
                ('idBs_RW_defect_tp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BS.bs_rw_defect_tp', verbose_name='Вид неисправности')),
                ('idBs_RW_element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BS.bs_rw_element', verbose_name='Элемент осмотра')),
                ('iddepartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BS.bs_department', verbose_name='Подразделение')),
                ('iddepowner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BS.bs_depowner', verbose_name='Филиал')),
                ('idkmo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KMO.kmo', verbose_name='КМО')),
                ('idresponsible', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='KMO.kmo_responsible', verbose_name='Ответственный за  устранение')),
                ('idrwkilometr', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BS.bs_rwkilometr', verbose_name='км')),
                ('idrwsp', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='idrwstation', chained_model_field='idrwstation', on_delete=django.db.models.deletion.CASCADE, to='BS.bs_rwsp')),
                ('idrwstage', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BS.bs_rwstage', verbose_name='Перегон')),
                ('idrwstation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BS.bs_rwstation', verbose_name='Станция/Участок')),
                ('idrwway', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='idrwstation', chained_model_field='idrwstation', on_delete=django.db.models.deletion.CASCADE, to='BS.bs_rwway')),
            ],
            options={
                'verbose_name': 'позиция КМО',
                'verbose_name_plural': 'Список позиций КМО',
            },
        ),
    ]
