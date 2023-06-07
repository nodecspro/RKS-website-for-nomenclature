from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    login = forms.CharField(max_length=50, help_text='Логин')
    password = forms.CharField(max_length=50, help_text='Пароль')
