# Generated by Django 5.1.4 on 2025-01-21 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KMO', '0003_alter_kmodet_image_defect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kmodet',
            name='image_defect',
            field=models.ImageField(blank=True, upload_to='kmo_imgs/test/<function Kmodet.<lambda> at 0x000001A01A454A40>', verbose_name='Фотография неисправности'),
        ),
    ]
