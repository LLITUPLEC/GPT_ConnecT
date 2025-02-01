# Generated by Django 5.1.4 on 2025-01-31 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bar_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_object', models.CharField(max_length=8, verbose_name='Тип объекта')),
                ('idobject', models.CharField(max_length=18, verbose_name='id объекта')),
                ('src_bc', models.CharField(blank=True, max_length=18, null=True, verbose_name='QR-код')),
                ('s_create_user', models.CharField(max_length=25, verbose_name='Создатель')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('s_update_user', models.CharField(blank=True, max_length=25, null=True, verbose_name='Изменивший')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
            ],
            options={
                'verbose_name': 'QR-код',
                'verbose_name_plural': 'QR-коды',
            },
        ),
    ]
