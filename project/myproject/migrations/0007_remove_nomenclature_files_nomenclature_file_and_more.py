# Generated by Django 4.2.1 on 2023-06-05 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0006_file_remove_nomenclature_file_nomenclature_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nomenclature',
            name='files',
        ),
        migrations.AddField(
            model_name='nomenclature',
            name='file',
            field=models.FileField(default='', upload_to='files/', verbose_name='Файл номенклатуры'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='File',
        ),
    ]
