from django.db import models

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
    # Relación con Categoría (1 Categoría puede tener muchas Películas)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='peliculas'
    )

    def __str__(self):
        return self.titulo