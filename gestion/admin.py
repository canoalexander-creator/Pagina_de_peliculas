from django.contrib import admin
from .models import Categoria, Pelicula

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'categoria', 'director', 'anio')
    list_filter = ('categoria', 'anio')
    search_fields = ('titulo', 'director')