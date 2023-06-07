from django.contrib import messages  # Импортируем модуль сообщений Django
from django.contrib.auth.hashers import (  # Импортируем функции для работы с паролями
    check_password, make_password)
from django.contrib.auth.models import \
    User  # Импортируем модель пользователя Django
from django.http import HttpResponseNotFound  # Импортируем классы HTTP-ответов
from django.http import (FileResponse, HttpResponse, HttpResponseRedirect,
                         JsonResponse)
from django.shortcuts import (  # Импортируем функции для работы с запросами и шаблонами
    get_object_or_404, redirect, render)
from django.urls import \
    reverse  # Импортируем функцию reverse для генерации URL-адресов

from .models import *  # Импортируем модели из текущего пакета


# Функция представления для авторизации
def auth(request):
    if request.method == "POST":
        login = request.POST.get("login")
        password = request.POST.get("password")
        user = User.objects.filter(login=login).first()

        if user and check_password(password, user.password):
            response = redirect('http://127.0.0.1:8000/')
            response.set_cookie('login', user.login)
            response.set_cookie('entry', '1')
            return response

    return render(request, 'webapp/authorization.html')


# Функция представления для профиля пользователя
def profile(request):
    a = User.objects.get(login=request.COOKIES.get('login'))
    return render(request, 'webapp/profile.html', {"user": a})


# Функция представления для регистрации
def reg(request):
    if request.method == "POST":
        login = request.POST.get("login")
        user, created = User.objects.get_or_create(
            login=login,
            defaults={
                "password": make_password(request.POST.get("password")),
                "email": request.POST.get("email"),
                "name": request.POST.get("name"),
                "surname": request.POST.get("surname"),
                "patronymic": request.POST.get("patronymic"),
                "phone": request.POST.get("phone_number"),
                "department": request.POST.get("department"),
            })

        if not created:
            return HttpResponse("Пользователь с таким логином уже существует.")

        response = redirect('http://127.0.0.1:8000/')
        response.set_cookie('entry', '1')
        response.set_cookie('login', user.login)
        return response

    return render(request, 'webapp/registration.html')


# Функция представления для выхода из системы
def logout(request):
    response = HttpResponseRedirect('http://127.0.0.1:8000/')
    response.delete_cookie('entry')
    response.delete_cookie('login')
    return response


# Главная функция представления
def main(request):
    nomenclature = Nomenclature.objects.prefetch_related('files')
    for item in nomenclature:
        item.status = all(file.status for file in item.files.all())

    return render(request, 'webapp/body.html', {'nomenclature': nomenclature})


# Функция представления для деталей номенклатуры
def nomenclature_detail(request, link):
    nomenclature = get_object_or_404(Nomenclature, link=link)
    files = nomenclature.files.all()
    return render(request, 'webapp/nomenclature_detail.html', {
        'nomenclature': nomenclature,
        'files': files
    })


# Функция представления для создания номенклатуры
def create_nomenclature(request):
    if request.COOKIES.get('entry') == '1':
        return render(request, 'webapp/create_nomenclature.html')
    else:
        return redirect(reverse('login'))


# Функция представления для сохранения номенклатуры
def save_nomenclature(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        create_date = request.POST.get('create_date')
        files = request.FILES.getlist('files')

        # Проверяем расширения файлов
        allowed_extensions = ('.xlsx', '.xls')
        invalid_files = [
            file.name for file in files
            if not file.name.lower().endswith(allowed_extensions)
        ]
        if invalid_files:
            messages.error(
                request,
                f'Invalid file(s) found: {", ".join(invalid_files)}. Only .xlsx and .xls files are allowed.'
            )
            return redirect('create_nomenclature')

        try:
            login_cookie = request.COOKIES.get('login')
            user = User.objects.get(login=login_cookie)
        except User.DoesNotExist:
            return redirect(reverse('login'))

        nomenclature = Nomenclature.objects.create(name=name,
                                                   create_date=create_date,
                                                   create_by=user)

        for file in files:
            file_object = File.objects.create(name=file.name, file=file)
            nomenclature.files.add(file_object)

        return redirect('http://127.0.0.1:8000/')

    return render(request, 'create_nomenclature.html')


# Функция представления для загрузки файла
def file_download(request, filename):
    nomenclature = get_object_or_404(Nomenclature, file__name=filename)
    file_path = nomenclature.file.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True)


# Функция представления для добавления файлов к номенклатуре
def add_files(request, link):
    if request.COOKIES.get('entry') == '1':
        nomenclature = get_object_or_404(Nomenclature, link=link)
        if request.method == 'POST':
            files = request.FILES.getlist('files')
            for file in files:
                if not file.name.lower().endswith(('.xlsx', '.xls')):
                    messages.error(request,
                                   'Only .xlsx and .xls files are allowed.')
                    return redirect('nomenclature_detail', link=link)

                file_object = File.objects.create(name=file.name, file=file)
                nomenclature.files.add(file_object)

            return redirect('nomenclature_detail', link=link)

        return render(request, 'webapp/add_files_popup.html',
                      {'nomenclature': nomenclature})
    else:
        return redirect(reverse('login'))


# Функция представления для получения всех файлов
def get_all_files(request):
    files = File.objects.filter(status=True)
    file_list = []
    for file in files:
        file_data = {
            'name': file.name,
        }
        file_list.append(file_data)
    return JsonResponse(file_list, safe=False)


# Функция представления для замены файла
def replace_file(request):
    files = request.FILES.getlist('files')
    if request.method == 'POST':
        original_file_id = request.POST.get('originalFileId')
        similar_file_name = request.POST.get('similarFileName')

        try:
            original_file = File.objects.get(id=original_file_id)
            similar_file = File.objects.get(name=similar_file_name)
            Nomenclature.files.through.objects.filter(
                file_id=original_file.id).update(file_id=similar_file.id)
            Nomenclature.update_status()

            return JsonResponse({
                'success': True,
                'message': 'File replaced successfully',
            })
        except File.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'File not found',
            })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method',
        })


# Функция представления для обработки страницы 404
def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
