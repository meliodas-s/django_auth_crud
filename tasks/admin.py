from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    # Creo los campos que solo se pueden leer
    readonly_fields = ("created",)
    # Campos a mostrar
    list_display = ('title', 'description', 'created','user_owner')

# Register your models here.
admin.site.register(Task, TaskAdmin)
