from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from .models import Pelicula, Categoria, Resena
from .forms import PeliculaForm, CategoriaForm, ResenaForm


def es_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# ==========================================
# AUTENTICACIÓN Y REGISTRO
# ==========================================

def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta fue creada.')
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Hola de nuevo, {user.username}!')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('inicio')


# ==========================================
# INICIO Y DASHBOARD ADMINISTRATIVO (SPRINT 3)
# ==========================================

def inicio(request):
    categorias = Categoria.objects.all()
    peliculas = Pelicula.objects.select_related('categoria').all()
    peliculas_recientes = peliculas.order_by('-id')[:6]
    return render(request, 'inicio.html', {
        'categorias': categorias,
        'peliculas': peliculas,
        'peliculas_recientes': peliculas_recientes,
        'total_peliculas': peliculas.count(),
        'total_categorias': categorias.count(),
    })


@user_passes_test(es_admin, login_url='login')
def dashboard_admin(request):
    total_peliculas = Pelicula.objects.count()
    total_categorias = Categoria.objects.count()
    total_resenas = Resena.objects.count()
    total_usuarios = User.objects.count()

    peliculas_recientes = Pelicula.objects.select_related('categoria').order_by('-id')[:5]
    categorias_con_conteo = Categoria.objects.annotate(num_peliculas=Count('peliculas')).order_by('-num_peliculas')
    resenas_recientes = Resena.objects.select_related('pelicula', 'usuario').order_by('-fecha_creacion')[:5]

    return render(request, 'dashboard.html', {
        'total_peliculas': total_peliculas,
        'total_categorias': total_categorias,
        'total_resenas': total_resenas,
        'total_usuarios': total_usuarios,
        'peliculas_recientes': peliculas_recientes,
        'categorias_con_conteo': categorias_con_conteo,
        'resenas_recientes': resenas_recientes,
    })


# ==========================================
# CRUD DE PELÍCULAS
# ==========================================

def lista_peliculas(request):
    peliculas = Pelicula.objects.select_related('categoria').all().order_by('-id')
    categorias = Categoria.objects.all()
    return render(request, 'lista_peliculas.html', {
        'peliculas': peliculas,
        'categorias': categorias,
    })


@user_passes_test(es_admin, login_url='login')
def crear_pelicula(request):
    if request.method == 'POST':
        form = PeliculaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Película agregada correctamente.')
            return redirect('lista_peliculas')
    else:
        form = PeliculaForm()
    return render(request, 'form_pelicula.html', {'form': form, 'accion': 'Agregar'})


@user_passes_test(es_admin, login_url='login')
def editar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        form = PeliculaForm(request.POST, instance=pelicula)
        if form.is_valid():
            form.save()
            messages.success(request, 'Película actualizada correctamente.')
            return redirect('lista_peliculas')
    else:
        form = PeliculaForm(instance=pelicula)
    return render(request, 'form_pelicula.html', {'form': form, 'accion': 'Editar'})


@user_passes_test(es_admin, login_url='login')
def eliminar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    if request.method == 'POST':
        pelicula.delete()
        messages.success(request, 'Película eliminada correctamente.')
        return redirect('lista_peliculas')
    return render(request, 'confirmar_eliminar.html', {
        'objeto': pelicula.titulo,
        'tipo': 'película',
        'url_cancelar': 'lista_peliculas'
    })


# ==========================================
# CRUD DE CATEGORÍAS
# ==========================================

def lista_categorias(request):
    categorias = Categoria.objects.all().order_by('nombre')
    return render(request, 'lista_categorias.html', {'categorias': categorias})


@user_passes_test(es_admin, login_url='login')
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'form_categoria.html', {'form': form, 'accion': 'Agregar'})


@user_passes_test(es_admin, login_url='login')
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'form_categoria.html', {'form': form, 'accion': 'Editar'})


@user_passes_test(es_admin, login_url='login')
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('lista_categorias')
    return render(request, 'confirmar_eliminar.html', {
        'objeto': categoria.nombre,
        'tipo': 'categoría',
        'url_cancelar': 'lista_categorias'
    })


# ==========================================
# CRUD DE RESEÑAS Y CALIFICACIONES (TAREA 2)
# ==========================================

def detalle_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)
    resenas = pelicula.resenas.select_related('usuario').all()
    ya_reseno = request.user.is_authenticated and resenas.filter(usuario=request.user).exists()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para dejar una reseña.')
            return redirect('login')
        if ya_reseno:
            messages.warning(request, 'Ya publicaste una reseña para esta película. Puedes editarla abajo.')
            return redirect('detalle_pelicula', pk=pk)

        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.pelicula = pelicula
            resena.usuario = request.user
            resena.save()
            messages.success(request, '¡Tu reseña y calificación se publicaron correctamente!')
            return redirect('detalle_pelicula', pk=pk)
    else:
        form = ResenaForm()

    return render(request, 'detalle_pelicula.html', {
        'pelicula': pelicula,
        'resenas': resenas,
        'form': form,
        'ya_reseno': ya_reseno,
    })


@login_required
def editar_resena(request, pk):
    resena = get_object_or_404(Resena, pk=pk)
    if resena.usuario != request.user and not es_admin(request.user):
        messages.error(request, 'No tienes permiso para editar esta reseña.')
        return redirect('detalle_pelicula', pk=resena.pelicula.pk)

    if request.method == 'POST':
        form = ResenaForm(request.POST, instance=resena)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reseña actualizada correctamente.')
            return redirect('detalle_pelicula', pk=resena.pelicula.pk)
    else:
        form = ResenaForm(instance=resena)

    return render(request, 'form_resena.html', {'form': form, 'resena': resena})


@login_required
def eliminar_resena(request, pk):
    resena = get_object_or_404(Resena, pk=pk)
    pelicula_pk = resena.pelicula.pk
    if resena.usuario != request.user and not es_admin(request.user):
        messages.error(request, 'No tienes permiso para eliminar esta reseña.')
        return redirect('detalle_pelicula', pk=pelicula_pk)

    if request.method == 'POST':
        resena.delete()
        messages.success(request, 'Reseña eliminada correctamente.')
        return redirect('detalle_pelicula', pk=pelicula_pk)

    return render(request, 'confirmar_eliminar.html', {
        'objeto': f'la reseña de "{resena.pelicula.titulo}"',
        'tipo': 'reseña',
        'url_cancelar': 'lista_peliculas'
    })