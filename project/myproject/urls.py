from django.conf import settings  # Импортируем модуль настроек Django
from django.conf.urls.static import \
    static  # Импортируем функцию static для обработки статических файлов
from django.contrib import admin  # Импортируем модуль администратора Django
from django.urls import \
    path  # Импортируем функцию path для определения маршрутов URL
from django.views.generic import \
    RedirectView  # Импортируем класс RedirectView для перенаправления URL

from .views import (  # Импортируем представления (views) из текущего пакета
    add_files, auth, create_nomenclature, file_download, get_all_files, logout,
    main, nomenclature_detail, pageNotFound, profile, reg, replace_file,
    save_nomenclature)

# Определяем маршруты URL
urlpatterns = [
    path('', main, name='main'),  # Главная страница
    path('login', RedirectView.as_view(
        url='/login/', permanent=True)),  # Перенаправление на страницу входа
    path('login/', auth, name='login'),  # Страница входа
    path('reg', RedirectView.as_view(
        url='/reg/',
        permanent=True)),  # Перенаправление на страницу регистрации
    path('reg/', reg, name='reg'),  # Страница регистрации
    path('admin/', admin.site.urls),  # URL для административной панели Django
    path('logout/', logout),  # URL для выхода из системы
    path('profile', RedirectView.as_view(
        url='/profile/',
        permanent=True)),  # Перенаправление на страницу профиля
    path('profile/', profile, name='profile'),  # Страница профиля
    path('nomenclature_info/<str:link>/',
         nomenclature_detail,
         name='nomenclature_detail'),  # Информация о номенклатуре
    path('nomenclature/add/', create_nomenclature,
         name='create_nomenclature'),  # Страница создания номенклатуры
    path('nomenclature/add_files/<str:link>/', add_files,
         name='add_files'),  # Загрузка файлов для номенклатуры
    path('nomenclature/save/', save_nomenclature,
         name='save_nomenclature'),  # Сохранение номенклатуры
    path('file_download/<str:filename>/', file_download,
         name='file_download'),  # Загрузка файла
    path('get_all_files/', get_all_files,
         name='get_all_files'),  # Получение списка всех файлов
    path('replace_file/', replace_file, name='replace_file'),  # Замена файла
]

# Если DEBUG режим включен в настройках Django, добавляем URL для обработки статических файлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound  # Устанавливаем обработчик для ошибки 404 (страница не найдена)
