import random  # Модуль для генерации случайной строки
import string  # Модуль для работы со строками

from django.db import models  # Модуль базы данных Django
from django.db.models.signals import (
    post_delete,  # Модуль сигналов Django
    post_save,
    pre_delete)
from django.dispatch import receiver  # Модуль обработчиков сигналов Django


# Класс пользователь
class User(models.Model):
    login = models.CharField('Логин', max_length=50)
    password = models.CharField('Пароль', max_length=50)
    email = models.EmailField('Почта', max_length=120)
    surname = models.CharField('Фамилия', max_length=40)
    name = models.CharField('Имя', max_length=35)
    patronymic = models.CharField('Отчество', max_length=45)
    phone = models.CharField('Телефон', max_length=18)
    department = models.IntegerField('Отдел')

    # Функция для отображения объектов класса в административной панели Django
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


def generate_random_link():
    # Функция для генерации случайной строки
    characters = string.ascii_letters + string.digits
    random_link = ''.join(random.choice(characters) for _ in range(10))
    return random_link


#  Класс номенклатура
class Nomenclature(models.Model):
    name = models.CharField('Название номенклатуры', max_length=255)
    create_date = models.DateTimeField("Дата и время создания",
                                       auto_now=False,
                                       auto_now_add=False)
    status = models.BooleanField('Статус', default=False)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.ManyToManyField('File')
    link = models.CharField('Сгенерированная ссылка',
                            max_length=10,
                            editable=False)

    class Meta:
        """
        Функция для отображения объектов класса в административной панели Django
        """
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатуры'

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения модели Nomenclature.
        Генерирует случайную ссылку перед сохранением объекта в базе данных.
        """
        if not self.link:
            self.link = generate_random_link()
        super().save(*args, **kwargs)


class File(models.Model):
    name = models.CharField('Название файла', max_length=100)
    file = models.FileField('Адрес файла', upload_to='files/')
    status = models.BooleanField('Статус', default=False)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения модели File.
        Вызывает обновление статуса номенклатуры после сохранения файла.
        """
        super().save(*args, **kwargs)
        self.update_nomenclature_status()

    def update_nomenclature_status(self):
        """
        Обновляет статус номенклатуры на основе статусов файлов, связанных с ней.
        """
        has_files_with_false_status = self.nomenclature_set.filter(
            files__status=False).exists()
        self.nomenclature_set.update(status=not has_files_with_false_status)


def set_nomenclature_link(sender, instance, **kwargs):
    """
    Сигнальная функция для установки сгенерированной ссылки для объекта Nomenclature перед сохранением.
    """
    if not instance.link:
        instance.link = generate_random_link()


@receiver(post_save, sender=(File, Nomenclature))
def handle_file_update(sender, instance, **kwargs):
    """
    Сигнальная функция для обновления статуса номенклатуры после сохранения или обновления файла или номенклатуры.
    """
    instance.update_nomenclature_status()


@receiver(post_delete, sender=Nomenclature)
@receiver(pre_delete, sender=Nomenclature)
def delete_files(sender, instance, **kwargs):
    """
    Сигнальная функция для удаления файлов, связанных с объектом Nomenclature, перед или после удаления.
    """
    files = instance.files.all()
    for file in files:
        file.file.delete(save=False)


@receiver(pre_delete, sender=Nomenclature)
def delete_associated_files(sender, instance, **kwargs):
    """
    Сигнальная функция для удаления связанных файлов, связанных с объектом Nomenclature, перед удалением.
    """
    files = instance.files.all()
    for file in files:
        file.delete()


post_delete.connect(delete_files, sender=Nomenclature)
