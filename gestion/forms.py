from django import forms
from .models import Categoria, Pelicula, Resena




class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Ciencia Ficción'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción breve de la categoría'}),
        }


    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre de la categoría debe tener al menos 3 caracteres.")
        return nombre




class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula
        fields = ['titulo', 'director', 'anio', 'sinopsis', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la película'}),
            'director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del director'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 2024'}),
            'sinopsis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe la sinopsis...'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }


    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo', '').strip()
        if len(titulo) < 2:
            raise forms.ValidationError("El título debe tener al menos 2 caracteres.")
        return titulo


    def clean_anio(self):
        anio = self.cleaned_data.get('anio')
        if anio and (anio < 1888 or anio > 2030):
            raise forms.ValidationError("Ingresa un año válido (entre 1888 y 2030).")
        return anio




class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.Select(
                choices=[
                    (5, '⭐⭐⭐⭐⭐ (5 - Excelente)'),
                    (4, '⭐⭐⭐⭐ (4 - Muy buena)'),
                    (3, '⭐⭐⭐ (3 - Buena)'),
                    (2, '⭐⭐ (2 - Regular)'),
                    (1, '⭐ (1 - Mala)')
                ],
                attrs={'class': 'form-select bg-dark text-light border-secondary'}
            ),
            'comentario': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light border-secondary',
                'rows': 3,
                'placeholder': 'Escribe tu opinión sobre la película...'
            }),
        }
        labels = {
            'calificacion': 'Calificación',
            'comentario': 'Tu Reseña',
        }