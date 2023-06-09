# Generated by Django 4.2.1 on 2023-06-05 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0002_alter_user_department'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nomenclature',
            options={'verbose_name': 'Номенклатура', 'verbose_name_plural': 'Номенклатуры'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Сотрудник', 'verbose_name_plural': 'Сотрудники'},
        ),
        migrations.AddField(
            model_name='nomenclature',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Статус'),
        ),
    ]
