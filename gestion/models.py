from django.db import models

class Integrante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    rol = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Proyecto(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    # Relación N:M (Muchos a Muchos)
    integrantes = models.ManyToManyField(Integrante, related_name='proyectos')

    def __str__(self):
        return self.titulo


class Actividad(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_entrega = models.DateField(blank=True, null=True)
    
    # Relación 1:N (Uno a Muchos con Proyecto)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='actividades')
    
    # Relación 1:N (Uno a Muchos con Integrante responsable)
    responsable = models.ForeignKey(
        Integrante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actividades'
    )

    def __str__(self):
        return f"{self.nombre} - {self.proyecto.titulo}"
