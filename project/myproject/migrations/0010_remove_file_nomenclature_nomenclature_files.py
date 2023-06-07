# Generated by Django 4.2.1 on 2023-06-05 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myproject', '0009_remove_nomenclature_files_file_nomenclature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='nomenclature',
        ),
        migrations.AddField(
            model_name='nomenclature',
            name='files',
            field=models.ManyToManyField(to='myproject.file'),
        ),
    ]
