from django.contrib import admin
from .models import Categoria, Pelicula, Resena




@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)




@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'categoria', 'director', 'anio')
    list_filter = ('categoria', 'anio')
    search_fields = ('titulo', 'director')




@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('id', 'pelicula', 'usuario', 'calificacion', 'fecha_creacion')
    list_filter = ('calificacion', 'fecha_creacion')
    search_fields = ('pelicula__titulo', 'usuario__username', 'comentario')