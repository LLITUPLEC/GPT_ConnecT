# Generated by Django 5.1.4 on 2025-01-31 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qrgenerator', '0008_bar_code_idrwway_alter_bar_code_idobject_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bar_code',
            name='idobject',
        ),
    ]
