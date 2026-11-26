from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pelicula, Categoria

# Vista protegida: solo usuarios autenticados pueden entrar
@login_required(login_url='login')
def inicio(request):
    peliculas = Pelicula.objects.select_related('categoria').all()
    categorias = Categoria.objects.all()
    return render(request, 'inicio.html', {
        'peliculas': peliculas,
        'categorias': categorias
    })

# 1. Registro de nuevos usuarios
def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'¡Cuenta creada con éxito para {usuario.username}! Ahora inicia sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

# 2. Inicio de sesión
def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 3. Cerrar sesión
def logout_usuario(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Pelicula, Categoria
from .forms import PeliculaForm, CategoriaForm

# Verificación de rol administrador en el servidor
def es_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# ==========================================
# CRUD DE PELÍCULAS (SPRINT 3 - TAREA 1)
# ==========================================

def es_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def lista_peliculas(request):
    peliculas = Pelicula.objects.select_related('categoria').all().order_by('-id')
    return render(request, 'lista_peliculas.html', {'peliculas': peliculas})


@login_required
@user_passes_test(es_admin)
def crear_pelicula(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        if form.is_valid():
            pelicula = form.save()
            messages.success(request, f'Película "{pelicula.titulo}" registrada correctamente.')
            return redirect('lista_peliculas')
    else:
        form = PeliculaForm()
    return render(request, 'form_pelicula.html', {'form': form, 'accion': 'Registrar Nueva Película'})


@login_required
@user_passes_test(es_admin)
def editar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        form = PeliculaForm(request.POST, instance=pelicula)
        if form.is_valid():
            form.save()
            messages.success(request, f'Película "{pelicula.titulo}" actualizada correctamente.')
            return redirect('lista_peliculas')
    else:
        form = PeliculaForm(instance=pelicula)
    return render(request, 'form_pelicula.html', {'form': form, 'accion': f'Editar: {pelicula.titulo}'})


@login_required
@user_passes_test(es_admin)
def eliminar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        titulo = pelicula.titulo
        pelicula.delete()
        messages.success(request, f'Película "{titulo}" eliminada correctamente.')
        return redirect('lista_peliculas')
    return render(request, 'confirmar_eliminar.html', {
        'objeto': pelicula,
        'tipo': 'película',
        'url_cancelar': 'lista_peliculas'
    })


# ==========================================
# CRUD DE CATEGORÍAS (SPRINT 3 - TAREA 1)
# ==========================================

def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'lista_categorias.html', {'categorias': categorias})


@login_required
@user_passes_test(es_admin)
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada correctamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'form_categoria.html', {'form': form, 'accion': 'Registrar Nueva Categoría'})


@login_required
@user_passes_test(es_admin)
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" actualizada correctamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'form_categoria.html', {'form': form, 'accion': f'Editar: {categoria.nombre}'})


@login_required
@user_passes_test(es_admin)
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre = categoria.nombre
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada correctamente.')
        return redirect('lista_categorias')
    return render(request, 'confirmar_eliminar.html', {
        'objeto': categoria,
        'tipo': 'categoría',
        'url_cancelar': 'lista_categorias'
    })