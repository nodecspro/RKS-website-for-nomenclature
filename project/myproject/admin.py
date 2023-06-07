from django.contrib import admin

from .models import File, Nomenclature, User

# Register your models here.
admin.site.register(User)
admin.site.register(Nomenclature)
admin.site.register(File)