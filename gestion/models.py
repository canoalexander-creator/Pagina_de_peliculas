from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg




class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)


    def __str__(self):
        return self.nombre




class Pelicula(models.Model):
    titulo = models.CharField(max_length=200)
    director = models.CharField(max_length=100, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    sinopsis = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='peliculas'
    )


    def __str__(self):
        return self.titulo


    def promedio_calificacion(self):
        promedio = self.resenas.aggregate(Avg('calificacion'))['calificacion__avg']
        return round(promedio, 1) if promedio else 0




class Resena(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='resenas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resenas')
    calificacion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(max_length=500)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-fecha_creacion']
        unique_together = ('pelicula', 'usuario')


    def __str__(self):
        return f"{self.usuario.username} - {self.pelicula.titulo} ({self.calificacion}★)"