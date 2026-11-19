from django.contrib import admin
from .models import Integrante, Proyecto, Actividad

@admin.register(Integrante)
class IntegranteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'correo', 'rol')
    list_filter = ('rol',)
    search_fields = ('nombre', 'apellido', 'correo', 'rol')

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'fecha_inicio', 'fecha_fin')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('titulo', 'descripcion')

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'proyecto', 'responsable', 'estado', 'fecha_entrega')
    list_filter = ('estado', 'proyecto', 'responsable', 'fecha_entrega')
    search_fields = ('nombre', 'descripcion', 'proyecto__titulo', 'responsable__nombre')